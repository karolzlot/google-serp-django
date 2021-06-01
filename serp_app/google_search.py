from bs4 import BeautifulSoup
import re
import requests
from .search_result import SearchResultDataclass,PopularWordDataclass,LinkDataclass
from collections import Counter


class GoogleSearch():
    
    @staticmethod
    def search(query,browser='chrome',only_links=False):

        google_search_url  = "https://www.google.pl/search?lr=lang_pl&num=30&q="+query

        if browser=='chrome':
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'
        elif browser=='firefox':
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0'
        else:
            raise ValueError("unhandled value of 'browser' argument ")

        headers = {
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': user_agent,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Accept-Language': 'en-US,en;q=0.9',
            }

        response = requests.get(google_search_url, headers=headers)

        html = response.text
        soup = BeautifulSoup(html, 'html.parser')


        result_stats_txt = soup.find('div',{'id':'result-stats'}).text.replace(u'\xa0', u' ').replace(u' ', u'')
        result_stats = int(re.search(r'\d+', result_stats_txt).group())

        search_results = soup.findAll('div',{'class':'tF2Cxc'})

        count = 0


        links=[]
        all_descriptions=''
        for result in search_results:
            
            try:
                links.append(LinkDataclass(link=result.find('a')['href'],position=count+1))
                all_descriptions+=' '+result.find('h3').text
                try:
                    all_descriptions+=' '+result.find('div',{'class':'IsZvec'}).text
                except:
                    all_descriptions+=' '+result.find('span').text

            except:
                continue

            count += 1
            if count >= 20:
                break
        
        if only_links:
            return links

        if count < 1:
            raise Exception('no google search results')

        popular_word_dataclasses = GoogleSearch.most_common_words(all_descriptions)


        search_results=SearchResultDataclass(
            query=query,
            results_total=result_stats,
            most_popular_words=popular_word_dataclasses,
            links=links,

        )

        return search_results

    @staticmethod
    def most_common_words(text):

        text_without_special_chars=re.sub(r'\W+', ' ', text)
        text_only_letters=''.join([i for i in text_without_special_chars if not i.isdigit()]).lower()
        
        words = text_only_letters.split()

        words_counter = Counter(words)

        popular_words = words_counter.most_common(10)

        from .search_result import PopularWordDataclass
        popular_word_dataclasses = [PopularWordDataclass(word=i[0],occurances=i[1]) for i in popular_words]

        return popular_word_dataclasses
                
    @staticmethod
    def multiple_search(queries,browser='chrome'): # zadanie dodatkowe
        multiple_search_results=[]

        for query in queries:
            searchresult={
                'query':query,
                'links':GoogleSearch.search(query,browser,only_links=True)
            }
            multiple_search_results.append(searchresult)
        
        return multiple_search_results

        


# if __name__ == "__main__":
#     # GoogleSearch.search('onet')
#     GoogleSearch.multiple_search(['onet','kawa','piłka'])
#     # GoogleSearch.search('onet',browser='firefox')

