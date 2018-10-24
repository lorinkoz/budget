# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import template
from django.template.defaultfilters import floatformat
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(needs_autoescape=True)
def money(value, extra="", autoescape=None):
    negative = value < 0
    dec = floatformat(abs(value), 2)
    format = "<span class='text-danger'><b>(%s)</b></span>" if negative else "%s"
    return mark_safe(format % dec)
