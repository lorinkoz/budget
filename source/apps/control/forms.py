# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms

from . import models
from apps.core.models import Area
from common.utils.years import get_perspective_years


class PlanForm(forms.ModelForm):

    class Meta:
        model = models.Plan
        fields = ('year', 'destination', 'amount')


class RecordForm(forms.ModelForm):

    class Meta:
        model = models.Record
        fields = ('date', 'destination', 'concept', 'amount', 'currency', 'description', 'plan')


class FundingForm(forms.ModelForm):

    class Meta:
        model = models.Funding
        fields = ('date', 'element', 'amount', 'currency', 'description')


class PlanAreaForm(forms.Form):

	YEARS = get_perspective_years()

	area = forms.ModelChoiceField(label='Area', queryset=Area.objects.all())
	year = forms.ChoiceField(label='Año', choices=YEARS, initial=YEARS[1][0])
