# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.validators import ValidationError
from django.utils.encoding import python_2_unicode_compatible

from common.constants import CURRENCIES
from common.validators import zero_validator, positive_validator
from common.utils.years import get_years


class YUIDManager(models.Manager):
    def get_by_natural_key(self, yuid, year):
        return self.get(yuid=yuid, date__year=year)


@python_2_unicode_compatible
class YUIDModel(models.Model):

    yuid = models.PositiveIntegerField(verbose_name='registro', unique_for_year='date', help_text='Identificador único en el año')
    date = models.DateField(verbose_name='fecha', help_text='Fecha de emisión')

    amount = models.DecimalField(verbose_name='importe', max_digits=20, decimal_places=2, validators=[zero_validator], help_text='Importe de la entrada')
    currency = models.CharField(verbose_name='moneda', max_length=3, choices=CURRENCIES, help_text='Moneda de la entrada')
    description = models.TextField(verbose_name='descripción', blank=True, help_text='Descripción de la entrada')

    objects = YUIDManager()

    class Meta:
        abstract = True
        ordering = ('-date', '-yuid')

    def __str__(self):
        return '%s - %s' % (self.yuid, self.date.year)

    def natural_key(self):
        return (self.yuid, self.date.year)

    def clean(self):
        # Year cannot be changed
        if self.pk:
            other = type(   self).objects.get(pk=self.pk)
            if other.date.year != self.date.year:
                raise ValidationError('No se puede modificar el año de un registro después de guardado.')
        # YUID must be auto-generated
        if not self.yuid and self.date:
            reference = type(self).objects.filter(date__year=self.date.year).order_by('-yuid').first()
            self.yuid = reference.yuid + 1 if reference else 1

    @property
    def html_id(self):
        return '%s-%s' % (self.yuid, self.date.year)


class Record(YUIDModel):

    STATUS = (
        (None, 'Pendiente'),
        (True, 'Confirmado'),
        (False, 'Cancelado'),
    )

    PLANS = get_years()

    destination = models.ForeignKey('core.Destination', verbose_name='destino', related_name='records', help_text='Destino de gasto asociado')
    concept = models.ForeignKey('core.Concept', verbose_name='concepto', related_name='records', limit_choices_to = {'status': True}, help_text='Concepto por el cual se emite el registro')
    plan = models.PositiveIntegerField(verbose_name='plan', choices=PLANS, default=PLANS[0][0], help_text='Plan anual asociado')

    status = models.NullBooleanField(verbose_name='estado', default=None, choices=STATUS, help_text='Estado del registro')

    class Meta(YUIDModel.Meta):
        verbose_name = 'registro'
        verbose_name_plural = 'registros'

    @property
    def is_confirmed(self):
        return self.status == True

    @property
    def is_cancelled(self):
        return self.status == False

    @property
    def is_pending(self):
        return self.status == None

    # def get_absolute_url(self):
        # return ('record_edit', [self.date.year, self.yuid])


class Funding(YUIDModel):

    element = models.ForeignKey('core.Element', verbose_name='elemento de gasto', related_name='fundings', limit_choices_to = {'parent': None}, help_text='Elemento de gasto al que esta asignación acredita')

    class Meta(YUIDModel.Meta):
        verbose_name = 'asignación de fondos'
        verbose_name_plural = 'asignaciones de fondos'


# @receiver(post_save, sender=Record)
# def auto_create_plan(sender, instance, created, **kwargs):
#     Plan.objects.get_or_create(year=instance.plan, destination=instance.destination)


class PlanManager(models.Manager):
    def get_by_natural_key(self, year, code):
        return self.get(year=year, destination__code=code)


@python_2_unicode_compatible
class Plan(models.Model):

    PLANS = get_years()

    year = models.PositiveIntegerField(verbose_name='año', choices=PLANS, default=PLANS[0][0], help_text='Año del plan')
    destination = models.ForeignKey('core.Destination', verbose_name='destino', related_name='plans', help_text='Destino de gasto asociado')

    amount = models.DecimalField(verbose_name='plan', max_digits=20, decimal_places=2, default=0, validators=[positive_validator], help_text='Monto del plan')

    objects = PlanManager()

    class Meta:
        verbose_name = 'plan'
        verbose_name_plural = 'planes'
        unique_together = ('destination', 'year')
        ordering = ('-year', 'destination')

    def __str__(self):
        return '%s / %s ' % (self.year, self.destination.friendly_name)

    def natural_key(self):
        return (self.year, self.destination.code)

    @property
    def html_id(self):
        return '%s-%s' % (self.year, self.destination.code)
