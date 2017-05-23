from django.conf.urls import  url
#from django.views.generic.base import TemplateView
from app.staff.operators import dea_overview, dea_execute_query


urlpatterns = [  

    url(r'^$', dea_execute_query),
    url(r'^overview/$', dea_overview),

    #url(r'^lockk/$', TemplateView.as_view(template_name='lockdown/form.html')),

]
