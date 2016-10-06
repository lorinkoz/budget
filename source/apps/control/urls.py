# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, include, url

from . import views


urlpatterns = patterns('',
    
    # url(r'^planes/$', views.PlanList.as_view(), name='plan_list'),
    # url(r'^planes/agregar/$', views.PlanCreate.as_view(), name='plan_create'),
    # url(r'^planes/editar/(?P<year>\d+)/(?P<code>[\w-]+)/$', views.PlanUpdate.as_view(), name='plan_update'),
    # url(r'^planes/eliminar/(?P<year>\d+)/(?P<code>[\w-]+)/$', views.PlanDelete.as_view(), name='plan_delete'),

    url(r'^planificar/$', views.PlanAreaSelector.as_view(), name='plan_area_selector'),
    url(r'^planificar/(?P<slug>[\w-]+)/(?P<year>actual|proximo)/$', views.PlanArea.as_view(), name='plan_area'),

    url(r'^registros/$', views.RecordList.as_view(), name='record_list'),
    url(r'^registros/pendientes/$', views.PendingRecordList.as_view(), name='pending_record_list'),
    url(r'^registros/confirmados/$', views.ConfirmedRecordList.as_view(), name='confirmed_record_list'),
    url(r'^registros/cancelados/$', views.CancelledRecordList.as_view(), name='cancelled_record_list'),
    url(r'^registros/comprometidos/$', views.CompromisedRecordList.as_view(), name='compromised_record_list'),
    url(r'^registros/agregar/$', views.RecordCreate.as_view(), name='record_create'),
    url(r'^registros/editar/(?P<year>\d+)/(?P<yuid>\d+)/$', views.RecordUpdate.as_view(), name='record_update'),
    url(r'^registros/confirmar/(?P<year>\d+)/(?P<yuid>\d+)/$', views.RecordConfirm.as_view(), name='record_confirm'),
    url(r'^registros/cancelar/(?P<year>\d+)/(?P<yuid>\d+)/$', views.RecordCancel.as_view(), name='record_cancel'),
    # url(r'^registros/restablecer/(?P<year>\d+)/(?P<yuid>\d+)/$', views.RecordReset.as_view(), name='record_reset'),
    # url(r'^registros/eliminar/(?P<year>\d+)/(?P<yuid>\d+)/$', views.RecordDelete.as_view(), name='record_delete'),
    
    url(r'^asignaciones/$', views.FundingList.as_view(), name='funding_list'),
    url(r'^asignaciones/agregar/$', views.FundingCreate.as_view(), name='funding_create'),
    url(r'^asignaciones/editar/(?P<year>\d+)/(?P<yuid>\d+)/$', views.FundingUpdate.as_view(), name='funding_update'),
    url(r'^asignaciones/eliminar/(?P<year>\d+)/(?P<yuid>\d+)/$', views.FundingDelete.as_view(), name='funding_delete'),
)
