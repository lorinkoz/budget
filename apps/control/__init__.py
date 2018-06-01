# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class CustomAppConfig(AppConfig):
    name = 'apps.control'
    verbose_name = 'Control'

default_app_config = 'apps.control.CustomAppConfig'



