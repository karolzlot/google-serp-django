from django.test import TestCase

# Create your tests here.

import datetime
from django.utils import timezone
from .models import Link_with_position, SearchResult
from django.test import Client
from .views import get_client_ip
from .google_search import GoogleSearch
import itertools
from .search_result import PopularWordDataclass 
from time import sleep


class RequestTests(TestCase):

    def test_local_ip(self):
        c = Client()
        response = c.get('/serp_app/')
        request = response.wsgi_request
        client_ip = get_client_ip(request)
        self.assert_(client_ip == '127.0.0.1')

    def test_request_without_request_parameters(self):
        c = Client()
        response = c.get('/serp_app/')
        self.assert_(response.status_code == 200)
        self.assert_(not b'Result:' in response.content) 

    def test_request_with_invalid_parameters(self):
        c = Client()
        response = c.get('/serp_app/', {'browser': 'netscape', 'query': 'Lewandowski'})
        self.assert_(response.status_code is 200)
        self.assert_(not b'Result:' in response.content) 
        self.assert_(b"Something is not working. That" in response.content) 

    def test_valid_request_and_various_recent_time_limit(self):
        c = Client()
        response = c.get('/serp_app/', {'browser': 'firefox', 'query': 'Robert'})
        self.assert_(response.status_code is 200)
        self.assert_(b'Result:' in response.content) 
        self.assert_(b"127.0.0.1" in response.content) 
        self.assert_(b"(20)." in response.content) 
        self.assert_(b"from cache: <b>False" in response.content) 
        self.assert_(not b"from cache: <b>True" in response.content) 

        sleep(1)
        # this is cached
        response = c.get('/serp_app/', {'browser': 'firefox', 'query': 'Robert', 'recent_time_limit': 20})
        self.assert_(response.status_code is 200)
        self.assert_(b'Result:' in response.content) 
        self.assert_(b"127.0.0.1" in response.content) 
        self.assert_(b"(20)." in response.content)
        self.assert_(not b"from cache: <b>False" in response.content) 
        self.assert_(b"from cache: <b>True" in response.content) 

        sleep(1)
        # this is not cached
        response = c.get('/serp_app/', {'browser': 'firefox', 'query': 'Robert', 'recent_time_limit': 1})
        self.assert_(response.status_code is 200)
        self.assert_(b'Result:' in response.content) 
        self.assert_(b"127.0.0.1" in response.content) 
        self.assert_(b"(20)." in response.content)
        self.assert_(b"from cache: <b>False" in response.content) 
        self.assert_(not b"from cache: <b>True" in response.content) 


class GoogleSearchClassTest(TestCase):
    def test_search(self):
        search_result=GoogleSearch.search('meble')
        self.assert_(search_result.results_total> 100000000)
        self.assert_(search_result.query== 'meble')
        self.assert_(search_result.most_popular_words.__len__()==10)
        self.assert_(search_result.links.__len__()==20)
        
    def test_most_common_words(self):
        words='a 4b b c .,c 432c 3d 3,42d$$ d;$ d'
        most_common_words=GoogleSearch._most_common_words(words,2)

        self.assert_(most_common_words.__len__()==2)
        self.assert_(most_common_words[0]==PopularWordDataclass(word='d',occurances=4))
        self.assert_(most_common_words[1]==PopularWordDataclass(word='c',occurances=3))
 
    def test_multiple_search(self):
        multiple_results= GoogleSearch.multiple_search(['kawa','piłka'])

        self.assert_(multiple_results.__len__()==2)
        self.assert_(multiple_results[0]['query']=='kawa')
        self.assert_(multiple_results[0]['links'].__len__()==20)
        self.assert_(multiple_results[1]['query']=='piłka')
        self.assert_(multiple_results[1]['links'].__len__()==20)

