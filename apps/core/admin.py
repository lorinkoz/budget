# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from common.admin import myadmin

from . import models


@admin.register(models.Area, site=myadmin)
class AreaAdmin(admin.ModelAdmin):
    search_fields = ('code', 'name')
    list_display = ('code', 'name')
    readonly_fields = ('slug',)


@admin.register(models.Element, site=myadmin)
class ElementAdmin(admin.ModelAdmin):
    search_fields = ('code', 'name', 'parent__code', 'parent__name')
    list_display = ('code', 'name', 'parent')


@admin.register(models.Destination, site=myadmin)
class DestinationAdmin(admin.ModelAdmin):
    search_fields = ('code', 'name', 'area__code', 'area__name')
    list_display = ('code', 'name', 'area', 'element', 'status')
    list_filter = ('status',)


@admin.register(models.Concept, site=myadmin)
class ConceptAdmin(admin.ModelAdmin):
    search_fields = ('code', 'name')
    list_display = ('code', 'name', 'positive', 'status')
    list_filter = ('positive', 'status',)