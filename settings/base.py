# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

path = lambda *x: os.path.join(BASE_DIR, *x)


BRAND_SHORT = 'Presupuesto'
BRAND_LONG = 'Sistema para la Gestión del Presupuesto'
VERSION = '2.0'

ADMINS = (('Lorenzo Peña', 'lorinkoz@uho.edu.cu'),)
MANAGERS = ADMINS


USE_I18N = True
USE_L10N = False
USE_TZ = True

LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/Havana'

DATE_INPUT_FORMATS = ['%d/%m/%Y', '%d/%m/%y', '%Y-%m-%d']


INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.admin',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'braces',
    'crispy_forms',

    'apps.core',
    'apps.users',
    'apps.control',
    'apps.reports',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

AUTH_USER_MODEL = 'users.User'

LOGIN_URL = 'user_login'
LOGOUT_URL = 'user_logout'

ROOT_URLCONF = 'common.urls'

STATICFILES_DIRS = (
    path('static'),
)

TEMPLATE_DIRS = (
    path('templates'),
)

LOCALE_PATHS = (
    path('locales'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.core.context_processors.request",
    "common.context_processors.constants",
)

CRISPY_TEMPLATE_PACK = 'bootstrap3'
