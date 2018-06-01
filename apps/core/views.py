# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models import Sum
from django.views.generic.base import TemplateView, RedirectView
from django.utils import timezone

from braces.views import SetHeadlineMixin

from .models import Area
from apps.control.models import Record
from common.mixins import ConsultorRequiredMixin, StaffRequiredMixin
from common.utils.assessment import assess_areas, assess_overdrawns


class SorterView(RedirectView):
    permanent = False

    def get_redirect_url(self):
        user = self.request.user
        if user.is_anonymous():
            return reverse(settings.LOGIN_URL)
        else:
            return reverse(user.get_absolute_url())


class BackendDashboard(StaffRequiredMixin, SetHeadlineMixin, TemplateView):
    headline = 'Panel de control'
    template_name = 'core/dashboard_backend.html'

    def get_context_data(self, **kwargs):
        context = super(BackendDashboard, self).get_context_data(**kwargs)
        this_year = timezone.now().year
        # Begin: no plan areas
        area_data = assess_areas(this_year, 12, False)
        area_data.pop()
        no_plan_areas = len(filter(lambda x: x.plan == 0 and x.book > 0, area_data))
        # End: no plan areas
        overdrawns = len(assess_overdrawns(this_year))-1
        stats = {
            'pending_records': Record.objects.filter(status=None).count(),
            'no_plan_areas': no_plan_areas,
            'overdrawns': overdrawns,
        }
        context['stats'] = stats
        context['year'] = this_year
        return context


class FrontendDashboard(ConsultorRequiredMixin, SetHeadlineMixin, TemplateView):
    headline = 'Resumen'
    template_name = 'core/dashboard_frontend.html'

    def get_context_data(self, **kwargs):
        context = super(FrontendDashboard, self).get_context_data(**kwargs)
        
        return context