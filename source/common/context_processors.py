# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings

def constants(request):
    return {
        'BRAND_SHORT': settings.BRAND_SHORT,
        'BRAND_LONG': settings.BRAND_LONG,
    }