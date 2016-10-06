# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from common.admin import myadmin

from . import models


@admin.register(models.Record, site=myadmin)
class RecordAdmin(admin.ModelAdmin):
    search_fields = (
    	'yuid', 'destination__code', 'destination__name',
    	'destination__area__code', 'destination__area__name',
    	'concept__code', 'concept__name', 'description'
    )
    list_display = ('yuid', 'date', 'destination', 'concept', 'amount', 'status')
    readonly_fields = ('yuid',)
    list_filter = ('status',)


@admin.register(models.Funding, site=myadmin)
class FundingAdmin(admin.ModelAdmin):
    search_fields = ('yuid', 'element__code', 'element__name')
    list_display = ('yuid', 'date', 'element', 'amount')
    filter_horizontal = ()
    readonly_fields = ('yuid',)


@admin.register(models.Plan, site=myadmin)
class PlanAdmin(admin.ModelAdmin):
    search_fields = ('year', 'destination__code', 'destination__name')
    list_display = ('year', 'destination', 'amount')