# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, include, url

from . import views


urlpatterns = patterns(
    "",
    url(r"^$", views.SorterView.as_view(), name="sorter"),
    url(r"^panel/$", views.BackendDashboard.as_view(), name="backend_dashboard"),
    url(r"^resumen/$", views.FrontendDashboard.as_view(), name="frontend_dashboard"),
)
