# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, include, url
from .admin import myadmin


urlpatterns = patterns(
    "",
    url(r"^", include("apps.core.urls")),
    url(r"^", include("apps.control.urls")),
    url(r"^", include("apps.users.urls")),
    url(r"^reportes/", include("apps.reports.urls")),
    url(r"^admin-interno/", include(myadmin.urls)),
)
