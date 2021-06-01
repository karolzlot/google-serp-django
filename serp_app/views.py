from django.shortcuts import render
from django.http import HttpResponse

from .models import SearchResult,PopularWord,Link_with_position
from django.utils import timezone
from .google_search import GoogleSearch

# Create your views here.

def index(request):

    if (request.GET.get('query') and request.GET.get('browser')):
        
        recent_time_limit=0
        try:
            recent_time_limit=int(request.GET.get('recent_time_limit'))
        except:
            pass

        datatime_recent_limit = timezone.now()-timezone.timedelta(seconds=recent_time_limit)
        recent_search_results =SearchResult.objects.filter(query=request.GET.get('query'),created_at__gt=datatime_recent_limit)
        if not recent_search_results:
            try:
                new_search_result = GoogleSearch.search(request.GET.get('query'),request.GET.get('browser'))
            except:
                return render(request, 'serp_app/serp_form.html', {
                'show_result':False,
                'error_message': "Something is not working. That's all we know."
                })

            result_db_object = SearchResult.objects.create(query = new_search_result.query,
                                                                results_total = new_search_result.results_total,
                                                                client_ip = get_client_ip(request))
            word_db_objects=[]                                                    
            for popular_word in new_search_result.most_popular_words:
                word_db_object= PopularWord.objects.create(word = popular_word.word,
                                        occurances = popular_word.occurances,
                                        search_result=result_db_object)
                word_db_objects.append(word_db_object)

            link_db_objects=[]   
            for link in new_search_result.links:
                link_db_object=Link_with_position.objects.create(link = link.link,
                                        position = link.position,
                                        search_result=result_db_object)
                link_db_objects.append(link_db_object)

            return render(request, 'serp_app/serp_form.html', {
                'show_result':True,
                'result_db_object': result_db_object,
                'word_db_objects': word_db_objects,
                'link_db_objects': link_db_objects,
                'from_cache': False,
                })
        else:
            result_db_object= recent_search_results[0]   

            word_db_objects = PopularWord.objects.filter(search_result=result_db_object)
            link_db_objects = Link_with_position.objects.filter(search_result=result_db_object)

            return render(request, 'serp_app/serp_form.html', {
                'show_result':True,
                'result_db_object': result_db_object,
                'word_db_objects': word_db_objects,
                'link_db_objects': link_db_objects,
                'from_cache': True
                })
                                    
    return render(request, 'serp_app/serp_form.html', {
        'show_result':False
        })



def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

