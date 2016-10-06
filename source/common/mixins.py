# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse

from braces.views import UserPassesTestMixin


class StaffRequiredMixin(UserPassesTestMixin):
    redirect_field_name = 'volver'

    def test_func(self, user):
        return user.is_staff

    def get_login_url(self):
        if self.request.user.is_authenticated(): 
            return reverse('sorter')
        return super(StaffRequiredMixin, self).get_login_url()


class ConsultorRequiredMixin(UserPassesTestMixin):
    redirect_field_name = 'volver'

    def test_func(self, user):
        return user.is_consultor

    def get_login_url(self):
        if self.request.user.is_authenticated(): 
            return reverse('sorter')
        return super(ConsultorRequiredMixin, self).get_login_url()

    def get_context_data(self, **kwargs):
        context = super(ConsultorRequiredMixin, self).get_context_data(**kwargs)
        context['my_areas'] = self.request.user.areas.all()
        return context