# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(help_text='C\xf3digo \xfanico asociado', max_length=10, verbose_name='c\xf3digo')),
                ('name', models.CharField(help_text='Nombre asociado', max_length=1024, verbose_name='nombre')),
            ],
            options={
                'verbose_name': '\xe1rea',
                'verbose_name_plural': '\xe1reas',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Concept',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(help_text='C\xf3digo \xfanico asociado', max_length=10, verbose_name='c\xf3digo')),
                ('name', models.CharField(help_text='Nombre asociado', max_length=1024, verbose_name='nombre')),
                ('status', models.BooleanField(default=True, help_text='Estado en el sistema', verbose_name='estado', choices=[(True, 'Activo'), (False, 'Inactivo')])),
                ('positive', models.BooleanField(default=True, help_text='Tipo de operaci\xf3n del concepto', verbose_name='tipo de operaci\xf3n', choices=[(True, 'Cr\xe9dito'), (False, 'D\xe9bito')])),
            ],
            options={
                'verbose_name': 'concepto',
                'verbose_name_plural': 'conceptos',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Destination',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(help_text='C\xf3digo \xfanico asociado', max_length=10, verbose_name='c\xf3digo')),
                ('name', models.CharField(help_text='Nombre asociado', max_length=1024, verbose_name='nombre')),
                ('status', models.BooleanField(default=True, help_text='Estado en el sistema', verbose_name='estado', choices=[(True, 'Activo'), (False, 'Inactivo')])),
                ('area', models.ForeignKey(related_name='destinations', verbose_name='area', to='core.Area', help_text='\xc1rea a la que pertenece este destino de gasto')),
            ],
            options={
                'verbose_name': 'destino de gasto',
                'verbose_name_plural': 'destinos de gasto',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Element',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(help_text='C\xf3digo \xfanico asociado', max_length=10, verbose_name='c\xf3digo')),
                ('name', models.CharField(help_text='Nombre asociado', max_length=1024, verbose_name='nombre')),
                ('creditable', models.BooleanField(default=False, help_text='Seleccione si el elemento acepta asignaciones de fondo', verbose_name='acepta asignaciones de fondo')),
                ('parent', models.ForeignKey(related_name='subelements', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='core.Element', help_text='Elemento padre', null=True, verbose_name='elemento padre')),
            ],
            options={
                'verbose_name': 'elemento de gasto',
                'verbose_name_plural': 'elementos de gasto',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='destination',
            name='element',
            field=models.ForeignKey(related_name='destinations', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='core.Element', help_text='Elemento de gasto al que pertenece este destino de gasto', null=True, verbose_name='elemento de gasto'),
            preserve_default=True,
        ),
    ]
