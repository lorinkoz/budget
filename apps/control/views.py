# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from functools import reduce

from django.db.models import Q, F, Sum
from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone

from braces.views import SetHeadlineMixin

from . import models, forms
from common.mixins import StaffRequiredMixin
from common.utils.assessment import assess_records
from apps.core.models import Area


class PlanAreaSelector(StaffRequiredMixin, SetHeadlineMixin, FormView):
    form_class = forms.PlanAreaForm
    headline = 'Planficar área'
    template_name = 'control/plan_area_selector.html'

    def form_valid(self, form):
        return redirect('plan_area', form.cleaned_data['area'].slug, form.cleaned_data['year'])


class PlanArea(StaffRequiredMixin, TemplateView):
    template_name = 'control/plan_area.html'

    def dispatch(self, request, slug, year):
        this_year = timezone.now().year
        years = {
            'anterior': this_year - 1,
            'actual': this_year,
            'proximo': this_year + 1,
        }
        self.year = years[year]
        self.area = get_object_or_404(Area, slug=slug)
        self.headline = 'Planificación %s (%s)' % (self.area.name, self.year)
        return super(PlanArea, self).dispatch(request, slug, year)

    def post(self, request, *args, **kwargs):
        for destination in self.area.destinations.order_by('-status','element__code'):
            for month in range(1, 13):
                plan, created = models.Plan.objects.get_or_create(year=self.year, month=month, destination=destination)
                try:
                    plan.amount = max(0, float(request.POST.get('%s::%s' % (destination.code, month))))
                    plan.save()
                except:
                    pass
        if self.year == timezone.now().year:
            deactivate = [x.pk for x in self.area.destinations.filter(plans__year=self.year).distinct().annotate(plan=Sum('plans__amount')).filter(plan=0)]
            self.area.destinations.exclude(pk__in=deactivate).update(status=True)
            self.area.destinations.filter(pk__in=deactivate).update(status=False)
        self.area.reorganize_destinations()
        return redirect(request.GET.get('volver', reverse('plan_area', args=[self.area.slug, self.kwargs['year']])))

    def get_context_data(self, **kwargs):
        context = super(PlanArea, self).get_context_data(**kwargs)
        plans = []
        for destination in self.area.destinations.all():
            dicto = {x.month: x.amount for x in destination.plans.filter(year=self.year)}
            sum = reduce(lambda t, p: t + p, dicto.values(), 0)
            plans.append((destination, [dicto.get(x, 0) for x in range(1, 13)] + [sum]))
        context['year'] = self.year
        context['area'] = self.area
        context['headline'] = self.headline
        context['plans'] = plans
        context['months'] = models.Plan.MONTHS
        return context


class RecordList(StaffRequiredMixin, SetHeadlineMixin, ListView):
    model = models.Record
    paginate_by = 25
    page_kwarg = 'p'
    headline = 'Registros'

    def get_template_names(self):
        template = 'control/record_list_print.html' if self.request.GET.get('print', False) else 'control/record_list.html'
        return [template]

    def get_queryset(self):
        queryset = super(RecordList, self).get_queryset().select_related('destination', 'destination__area', 'destination__element', 'concept')
        query = self.request.GET.get('q','')
        if query:
            queryset = queryset.filter(
                Q(yuid__iexact=query)|
                Q(destination__code__iexact=query)|
                Q(destination__name__icontains=query)|
                Q(destination__area__name__icontains=query)|
                Q(description__icontains=query)|
                Q(amount__iexact=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super(RecordList, self).get_context_data(**kwargs)
        context['total'] = -assess_records(self.get_queryset())
        if not 'print' in self.request.GET:
            qd = self.request.GET.copy()
            qd['print'] = True
            context['print_link'] = self.request.path + '?' + qd.urlencode()
        return context


class PendingRecordList(RecordList):
    queryset = models.Record.objects.filter(status=None)
    headline = 'Registros pendientes'


class ConfirmedRecordList(RecordList):
    queryset = models.Record.objects.filter(status=True)
    headline = 'Registros confirmados'


class CancelledRecordList(RecordList):
    queryset = models.Record.objects.filter(status=False)
    headline = 'Registros cancelados'


class CompromisedRecordList(RecordList):
    queryset = models.Record.objects.exclude(date__year=F('plan'))
    headline = 'Registros comprometidos'


class RecordCreate(StaffRequiredMixin, SetHeadlineMixin, CreateView):
    model = models.Record
    form_class = forms.RecordForm
    headline = 'Nuevo registro'
    template_name = 'control/record_form.html'

    def get_success_url(self):
        return self.request.GET.get('volver', reverse('record_list'))

    def get_initial(self):
        return {
            'currency': self.request.user.default_currency,
        }


class RecordUpdate(StaffRequiredMixin, SetHeadlineMixin, UpdateView):
    model = models.Record
    form_class = forms.RecordForm
    headline = 'Editar registro %s'
    template_name = 'control/record_form.html'

    def get_object(self):
        return self.model.objects.get(yuid=self.kwargs.get('yuid'), date__year=self.kwargs.get('year'))

    def get_headline(self):
        return self.headline % self.get_object()

    def get_success_url(self):
        return self.request.GET.get('volver', reverse('record_list'))

    def post(self, request, *args, **kwargs):
        if not self.get_object().is_pending:
            return redirect(self.get_success_url())
        return super(RecordUpdate, self).post(request, *args, **kwargs)


class RecordConfirm(StaffRequiredMixin, SetHeadlineMixin, DetailView):
    model = models.Record
    headline = 'Confirmar registro %s'
    template_name = 'control/record_confirm.html'

    def get_object(self):
        return self.model.objects.get(yuid=self.kwargs.get('yuid'), date__year=self.kwargs.get('year'))

    def get_headline(self):
        return self.headline % self.get_object()

    def post(self, request, *args, **kwargs):
        target = self.get_object()
        target.status = True
        target.save()
        return redirect(self.request.GET.get('volver', reverse('record_list')))


class RecordCancel(StaffRequiredMixin, SetHeadlineMixin, DetailView):
    model = models.Record
    headline = 'Cancelar registro %s'
    template_name = 'control/record_cancel.html'

    def get_object(self):
        return self.model.objects.get(yuid=self.kwargs.get('yuid'), date__year=self.kwargs.get('year'))

    def get_headline(self):
        return self.headline % self.get_object()

    def post(self, request, *args, **kwargs):
        target = self.get_object()
        target.status = False
        target.save()
        return redirect(self.request.GET.get('volver', reverse('record_list')))


class FundingList(StaffRequiredMixin, SetHeadlineMixin, ListView):
    model = models.Funding
    paginate_by = 25
    page_kwarg = 'p'
    headline = 'Asignaciones'
    template_name = 'control/funding_list.html'

    def get_queryset(self):
        queryset = super(FundingList, self).get_queryset()
        query = self.request.GET.get('q','')
        if query:
            queryset = queryset.filter(
                Q(yuid__iexact=query)|
                Q(element__code__iexact=query)|
                Q(element__name__icontains=query)|
                Q(description__icontains=query)|
                Q(amount__iexact=query)
            )
        return queryset


class FundingCreate(StaffRequiredMixin, SetHeadlineMixin, CreateView):
    model = models.Funding
    form_class = forms.FundingForm
    headline = 'Nueva asignación'
    template_name = 'control/funding_form.html'

    def get_success_url(self):
        return self.request.GET.get('volver', reverse('funding_list'))

    def get_initial(self):
        return {
            'currency': self.request.user.default_currency,
        }


class FundingUpdate(StaffRequiredMixin, SetHeadlineMixin, UpdateView):
    model = models.Funding
    form_class = forms.FundingForm
    headline = 'Editar asignación %s'
    template_name = 'control/funding_form.html'

    def get_object(self):
        return self.model.objects.get(yuid=self.kwargs.get('yuid'), date__year=self.kwargs.get('year'))

    def get_headline(self):
        return self.headline % self.get_object()

    def get_success_url(self):
        return self.request.GET.get('volver', reverse('funding_list'))


class FundingDelete(StaffRequiredMixin, SetHeadlineMixin, DeleteView):
    model = models.Funding
    headline = 'Eliminar asignación %s'
    template_name = 'control/funding_delete.html'

    def get_object(self):
        return self.model.objects.get(yuid=self.kwargs.get('yuid'), date__year=self.kwargs.get('year'))

    def get_headline(self):
        return self.headline % self.get_object()

    def get_success_url(self):
        return self.request.GET.get('volver', reverse('record_list'))
