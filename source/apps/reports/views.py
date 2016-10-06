# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404
from django.utils import timezone

from braces.views import SetHeadlineMixin

from . import forms
from common.utils import assessment
from common.mixins import ConsultorRequiredMixin, StaffRequiredMixin
from apps.core.models import Area, Element


class AreaSummary(StaffRequiredMixin, SetHeadlineMixin, TemplateView):
	headline = 'Resumen por áreas'
	template_name = 'reports/area_summary.html'

	def get_context_data(self, **kwargs):
	    context = super(AreaSummary, self).get_context_data(**kwargs)
	    filter_form = forms.ReportFilterForm(self.request.GET)
	    year, month, specific = filter_form.get_data()
	    context['year'] = year
	    context['data'] = assessment.assess_areas(year, month, specific)
	    context['filter'] = filter_form
	    return context


class AreaNoPlanSummary(StaffRequiredMixin, SetHeadlineMixin, TemplateView):
	headline = 'Areas sin planificar'
	template_name = 'reports/area_noplan_summary.html'

	def get_context_data(self, **kwargs):
	    context = super(AreaNoPlanSummary, self).get_context_data(**kwargs)
	    data = assessment.assess_areas(timezone.now().year, 12, False)
	    data.pop()
	    context['data'] = filter(lambda x: x.plan == 0 and x.book > 0, data)
	    return context


class AreaDetailed(StaffRequiredMixin, SetHeadlineMixin, DetailView):
	model = Area
	template_name = 'reports/area_detailed.html'

	def get_headline(self):
		return self.get_object().name

	def get_context_data(self, **kwargs):
	    context = super(AreaDetailed, self).get_context_data(**kwargs)
	    filter_form = forms.ReportFilterForm(self.request.GET)
	    year, month, specific = filter_form.get_data()
	    context['year'] = year
	    context['data'] = assessment.assess_area(self.get_object(), year, month, specific)
	    context['filter'] = filter_form
	    return context


class AreaConsultor(ConsultorRequiredMixin, SetHeadlineMixin, DetailView):
	model = Area
	template_name = 'reports/area_consultor.html'

	def get_headline(self):
		return self.get_object().name

	def test_func(self, user):
		test = super(AreaConsultor, self).test_func(user)
		return test and user.areas.filter(pk=self.get_object().pk).exists()

	def get_context_data(self, **kwargs):
	    context = super(AreaConsultor, self).get_context_data(**kwargs)
	    filter_form = forms.ReportFilterForm(self.request.GET)
	    year, month, specific = filter_form.get_data()
	    context['year'] = year
	    context['data'] = assessment.assess_area(self.get_object(), year, month, specific)
	    context['filter'] = filter_form
	    return context


class ElementSummary(StaffRequiredMixin, SetHeadlineMixin, TemplateView):
	headline = 'Resumen por elemento de gasto'
	template_name = 'reports/element_summary.html'

	def get_context_data(self, **kwargs):
	    context = super(ElementSummary, self).get_context_data(**kwargs)
	    filter_form = forms.ReportFilterForm(self.request.GET)
	    year, month, specific = filter_form.get_data()
	    context['year'] = year
	    context['data'] = assessment.assess_elements(year, month, specific)
	    context['filter'] = filter_form
	    return context


class ElementDetailed(StaffRequiredMixin, SetHeadlineMixin, DetailView):
	model = Element
	template_name = 'reports/element_detailed.html'

	def get_object(self):
		return get_object_or_404(self.model, code=self.kwargs['code'])

	def get_headline(self):
		return self.get_object().name

	def get_context_data(self, **kwargs):
	    context = super(ElementDetailed, self).get_context_data(**kwargs)
	    filter_form = forms.ReportFilterForm(self.request.GET)
	    year, month, specific = filter_form.get_data()
	    context['year'] = year
	    context['data'] = assessment.assess_element(self.get_object(), year, month, specific)
	    context['filter'] = filter_form
	    return context


class AvailabilityReport(StaffRequiredMixin, SetHeadlineMixin, TemplateView):
	headline = 'Disponibilidad de fondos'
	template_name = 'reports/availability.html'

	def get_context_data(self, **kwargs):
	    context = super(AvailabilityReport, self).get_context_data(**kwargs)
	    filter_form = forms.YearFilterForm(self.request.GET)
	    year = filter_form.get_year()
	    context['year'] = year
	    context['data'] = assessment.assess_availability(year)
	    context['filter'] = filter_form
	    return context


class OverdrawnsReport(StaffRequiredMixin, SetHeadlineMixin, TemplateView):
	headline = 'Destinos sobregirados'
	template_name = 'reports/overdrawns.html'

	def get_context_data(self, **kwargs):
	    context = super(OverdrawnsReport, self).get_context_data(**kwargs)
	    this_year = timezone.now().year
	    context['year'] = this_year
	    context['data'] = assessment.assess_overdrawns(this_year)
	    return context
