from time import sleep

from django.test import Client, TestCase

from .google_search import GoogleSearch
from .search_result import PopularWordDataclass
from .views import get_client_ip

# Create your tests here.



class RequestTests(TestCase):

    def test_local_ip(self):
        c = Client()
        response = c.get('/serp_app/')
        request = response.wsgi_request
        client_ip = get_client_ip(request)
        self.assertEqual(client_ip, '127.0.0.1')

    def test_request_without_request_parameters(self):
        c = Client()
        response = c.get('/serp_app/')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'Result:', response.content) 

    def test_request_with_invalid_parameters(self):
        c = Client()
        response = c.get('/serp_app/', {'browser': 'netscape', 'query': 'Lewandowski'})
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'Result:', response.content) 
        self.assertIn(b"Something is not working. That", response.content) 

    def test_valid_request_and_various_recent_time_limit(self):
        c = Client()
        response = c.get('/serp_app/', {'browser': 'firefox', 'query': 'Robert'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Result:', response.content) 
        self.assertIn(b"127.0.0.1", response.content) 
        self.assertIn(b"(20).", response.content) 
        self.assertIn(b"from cache: <b>False", response.content) 
        self.assertNotIn(b"from cache: <b>True", response.content) 

        sleep(1)
        # this is cached
        response = c.get('/serp_app/', {'browser': 'firefox', 'query': 'Robert', 'recent_time_limit': 20})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Result:', response.content) 
        self.assertIn(b"127.0.0.1", response.content) 
        self.assertIn(b"(20).", response.content)
        self.assertNotIn(b"from cache: <b>False", response.content) 
        self.assertIn(b"from cache: <b>True", response.content) 

        sleep(1)
        # this is not cached
        response = c.get('/serp_app/', {'browser': 'firefox', 'query': 'Robert', 'recent_time_limit': 1})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Result:', response.content) 
        self.assertIn(b"127.0.0.1", response.content) 
        self.assertIn(b"(20).", response.content)
        self.assertIn(b"from cache: <b>False", response.content) 
        self.assertNotIn(b"from cache: <b>True", response.content) 


class GoogleSearchClassTests(TestCase):
    def test_search(self):
        search_result=GoogleSearch.search('meble')
        self.assertGreater(search_result.results_total, 10000000)
        self.assertEqual(search_result.query, 'meble')
        self.assertEqual(len(search_result.most_popular_words), 10)
        self.assertEqual(len(search_result.links), 20)
        
    def test_most_common_words(self):
        words='a 4b b c .,c 432c 3d 3,42d$$ d;$ d'
        most_common_words=GoogleSearch._most_common_words(words,2)

        self.assertEqual(len(most_common_words), 2)
        self.assertEqual(most_common_words[0], PopularWordDataclass(word='d',occurances=4))
        self.assertEqual(most_common_words[1], PopularWordDataclass(word='c',occurances=3))
 
    def test_multiple_search(self):
        multiple_results= GoogleSearch.multiple_search(['kawa','piłka'])

        self.assertEqual(len(multiple_results), 2)
        self.assertEqual(multiple_results[0]['query'], 'kawa')
        self.assertEqual(len(multiple_results[0]['links']), 20)
        self.assertEqual(multiple_results[1]['query'], 'piłka')
        self.assertEqual(len(multiple_results[1]['links']), 20)
        self.assertNotEqual(multiple_results[0]['links'][0], multiple_results[1]['links'][0])

