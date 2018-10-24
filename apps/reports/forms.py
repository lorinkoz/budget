# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.utils import timezone

from common.utils.years import get_years


def get_months():
    now = timezone.now()
    basic = [
        [12, "Diciembre"],
        [11, "Noviembre"],
        [10, "Octubre"],
        [9, "Septiembre"],
        [8, "Agosto"],
        [7, "Julio"],
        [6, "Junio"],
        [5, "Mayo"],
        [4, "Abril"],
        [3, "Marzo"],
        [2, "Febrero"],
        [1, "Enero"],
    ]

    basic[-now.month][0] = ""
    return basic


VOLUME = (("", "Acumulativo hasta"), ("1", "Específico para"))


class ReportFilterForm(forms.Form):
    a = forms.ChoiceField(label="", choices=get_years(), required=False)
    s = forms.ChoiceField(label="", choices=VOLUME, required=False)
    m = forms.ChoiceField(label="", choices=get_months(), required=False)

    def get_data(self):
        now = timezone.now()
        if self.is_valid():
            try:
                year = int(self.cleaned_data.get("a"))
            except:
                year = now.year
            try:
                month = int(self.cleaned_data.get("m"))
            except:
                month = now.month
            specific = self.cleaned_data.get("s", False)
        else:
            year = now.year
            month = now.month
            specific = False
        return (year, month, specific)


class YearFilterForm(forms.Form):

    a = forms.ChoiceField(label="", choices=[(None, "Acumulativo")] + get_years(), required=False)

    def get_year(self):
        if self.is_valid():
            try:
                year = int(self.cleaned_data.get("a"))
            except:
                year = None
        else:
            year = None
        return year
