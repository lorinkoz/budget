# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, include, url

from . import views


urlpatterns = patterns('',
    
    url(r'^areas/$', views.AreaSummary.as_view(), name='area_summary'),
    url(r'^areas/sin-planificar/$', views.AreaNoPlanSummary.as_view(), name='area_noplan_summary'),
    url(r'^areas/(?P<slug>[\w-]+)/$', views.AreaDetailed.as_view(), name='area_detailed'),

    url(r'^elementos-de-gasto/$', views.ElementSummary.as_view(), name='element_summary'),
    url(r'^elementos-de-gasto/(?P<code>[\w-]+)/$', views.ElementDetailed.as_view(), name='element_detailed'),
    
    url(r'^disponibilidad/$', views.AvailabilityReport.as_view(), name='availability_report'),
    url(r'^destinos-sobregirados/$', views.OverdrawnsReport.as_view(), name='overdrawns_report'),
    
    url(r'^(?P<slug>[\w-]+)/$', views.AreaConsultor.as_view(), name='area_consultor'),
)
