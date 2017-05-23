'''
Created on 18/ott/2016

@author: Sab
'''

"""
  Testa le query su ElasticSearch
"""
import json
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse, HttpResponseBadRequest
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.conf import settings
from django.utils.safestring import mark_safe

from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import HtmlFormatter

from app.decorators import check_elastic_status
from inputs import AutoQuery, Exact, Clean

"""
"""
@check_elastic_status
def dea_overview(request):
    print ">>>> dea_overview"
    context = RequestContext(request)
    results = []

    # recupero l'istanza di elastic-search e il nome dell'indice
    es_client = settings.ES_CLIENT
    es_index_name = settings.ES_INDEX_NAME

    results.append(es_index_name)
    results.append(es_client.info())

    return JsonResponse(results, safe=False)
        

def data_prettified(instance):
    """Function to display pretty version of our data"""

    # Convert the data to sorted, indented JSON
    response = json.dumps(instance, sort_keys=True, indent=2)

    # Truncate the data. Alter as needed
    #response = response[:5000]

    # Get the Pygments formatter
    formatter = HtmlFormatter(style='colorful')

    # Highlight the data
    response = highlight(response, JsonLexer(), formatter)

    # Get the stylesheet
    style = "<style>" + formatter.get_style_defs() + "</style><br>"

    # Safe the output
    return mark_safe(style + response)

@check_elastic_status
def dea_execute_query(request):
    print ">>>> dea_execute_query"
    context = RequestContext(request)
    context_dict = {}

    if 'query' in request.GET:
        if str(Clean(request.GET['query'])) in [None, '']:
            return HttpResponseBadRequest('Error: Query input is null');

        es_client = settings.ES_CLIENT
        es_index_name = settings.ES_INDEX_NAME

        jquery = json.loads(request.GET['query'])

        res = es_client.search(index=es_index_name, body=jquery)
        
        results = []
        print("Got %d Hits:" % res['hits']['total'])
        for hit in res['hits']['hits']:
            results.append(hit["_source"])
    
        return JsonResponse(data_prettified(results), safe=False)
    
    return render_to_response('index.html', context_dict, context);
