# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .base import *


DEBUG = False
TEMPLATE_DEBUG = DEBUG

BRAND_SHORT = BRAND_SHORT + ' -stg-'

ALLOWED_HOSTS = ['10.26.16.8']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'presup',
        'USER': 'presup',
        'PASSWORD': 'stagingpresup',
        'HOST': '',
        'PORT': '',
    },
}

AUTHENTICATION_BACKENDS = (
    'apps.users.backends.OpenLdapUHOBackend',
    'django.contrib.auth.backends.ModelBackend',
)

STATIC_URL = '/presupuesto/static/'
STATIC_ROOT = path('../storage/static/')

SECRET_KEY = 'n&f^b01f=c5tm%=r77ylqqtzm9!p%lj(8*rv+jc3o)_1e-mtvb'