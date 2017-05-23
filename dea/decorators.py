from django.conf import settings
from django.http import HttpResponseRedirect
from elasticsearch import Elasticsearch
from elasticsearch import exceptions as es_exceptions


def check_elastic_status(function):
    def wrap(request, *args, **kwargs):
        # controllo lo stato della connessione a ElastiSearch
        try:
            es = Elasticsearch()
            es.info()
            return function(request, *args, **kwargs)
        except es_exceptions.ConnectionError as ce:
            return HttpResponseRedirect('/elastic-connection-error')
        except Exception as generic_exp:
            print str(generic_exp)
            return HttpResponseRedirect('/elastic-connection-error')

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
