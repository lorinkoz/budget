# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

from common.admin import myadmin

from . import models, forms


class AreaAuthorityInline(admin.TabularInline):
    model = models.AreaAuthority
    extra = 0


@admin.register(models.User, site=myadmin)
class UserAdmin(DefaultUserAdmin):
    inlines = (AreaAuthorityInline,)
    form = forms.AdminUserChangeForm
    add_form = forms.AdminUserCreationForm
    list_display = ('email', 'display_name', 'role',)
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = (
        ('Información básica', {'fields': ('email', 'display_name')}),
        ('Información de seguridad', {'fields': ('password', 'role')}),
        ('Otros datos', {'fields': ('default_currency',)}),
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'password1', 'password2')}),
    )
