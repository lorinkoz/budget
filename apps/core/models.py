# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
# from django.core.validators import ValidationError
from django.utils.encoding import python_2_unicode_compatible

from common.validators import code_validator
from common.snippets import fields as snippets


CODE_LENGTH = 10
NAME_LENGTH = 1024
FORMAT = '%s - %s'


class CodeManager(models.Manager):
    def get_by_natural_key(self, code):
        return self.get(code=code)


@python_2_unicode_compatible
class ModelWithCodeName(models.Model):

    code = models.CharField(verbose_name='código', max_length=CODE_LENGTH, validators=[code_validator], help_text='Código único asociado')
    name = models.CharField(verbose_name='nombre', max_length=NAME_LENGTH, help_text='Nombre asociado')

    objects = CodeManager()

    class Meta:
        abstract = True
        ordering = ('code', 'name')

    def __str__(self):
        return FORMAT % (self.code, self.name)

    def natural_key(self):
        return (self.code,)


class ModelWithStatus(models.Model):

    STATUS = (
        (True, 'Activo'),
        (False, 'Inactivo'),
    )

    status = models.BooleanField(verbose_name='estado', choices=STATUS, default=True, help_text='Estado en el sistema')

    class Meta:
        abstract = True


class Area(ModelWithCodeName):

    slug = snippets.AutoSlugField(verbose_name='slug', populate_from='name', overwrite=True)

    class Meta(ModelWithCodeName.Meta):
        verbose_name = 'área'
        verbose_name_plural = 'áreas'

    def reorganize_destinations(self):
        k = 1
        for destination in self.destinations.order_by('-status','element__code'):
            destination.code = '%s%s' % (self.code, ('%s' % k).rjust(2, '0'))
            destination.save()
            k += 1


class Element(ModelWithCodeName):

    parent = models.ForeignKey('self', verbose_name='elemento padre', null=True, blank=True, related_name='subelements', on_delete=models.SET_NULL, help_text='Elemento padre')

    class Meta(ModelWithCodeName.Meta):
        verbose_name = 'elemento de gasto'
        verbose_name_plural = 'elementos de gasto'

    @property
    def creditable(self):
        return self.parent is None


class Destination(ModelWithCodeName, ModelWithStatus):

    area = models.ForeignKey('Area', verbose_name='area', related_name='destinations', help_text='Área a la que pertenece este destino de gasto')
    element = models.ForeignKey('Element', verbose_name='elemento de gasto', blank=True, null=True, related_name='destinations', on_delete=models.SET_NULL, help_text='Elemento de gasto al que pertenece este destino de gasto')

    class Meta(ModelWithCodeName.Meta):
        verbose_name = 'destino de gasto'
        verbose_name_plural = 'destinos de gasto'

    @property
    def friendly_name(self):
        return '%s (%s)' % (self.name, self.area.name)


class Concept(ModelWithCodeName, ModelWithStatus):

    OPERATIONS = (
        (True, 'Crédito'),
        (False, 'Débito'),
    )

    positive = models.BooleanField('tipo de operación', choices=OPERATIONS, default=True, help_text='Tipo de operación del concepto')

    class Meta(ModelWithCodeName.Meta):
        verbose_name = 'concepto'
        verbose_name_plural = 'conceptos'
