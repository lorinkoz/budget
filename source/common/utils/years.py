# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils import timezone


def get_years():
    this_year = timezone.now().date().year
    years = range(2012, this_year + 1)
    years.reverse()
    return [(x,)*2 for x in years]


def get_perspective_years():
    this_year = timezone.now().date().year
    return (
    	('anterior', this_year - 1),
    	('actual', this_year),
    	('proximo', this_year + 1),
    )
