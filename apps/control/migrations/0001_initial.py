# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Funding',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('yuid', models.PositiveIntegerField(help_text='Identificador \xfanico en el a\xf1o', verbose_name='registro', unique_for_year='date')),
                ('date', models.DateField(help_text='Fecha de emisi\xf3n', verbose_name='fecha')),
                ('amount', models.DecimalField(help_text='Importe de la entrada', verbose_name='importe', max_digits=20, decimal_places=2, validators=[django.core.validators.MinValueValidator(1)])),
                ('description', models.TextField(help_text='Descripci\xf3n de la entrada', verbose_name='descripci\xf3n', blank=True)),
                ('element', models.ForeignKey(related_name='fundings', verbose_name='elemento de gasto', to='core.Element', help_text='Elemento de gasto al que esta asignaci\xf3n acredita')),
            ],
            options={
                'verbose_name': 'asignaci\xf3n de fondos',
                'verbose_name_plural': 'asignaciones de fondos',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('year', models.PositiveIntegerField(help_text='A\xf1o del plan', verbose_name='a\xf1o')),
                ('amount', models.DecimalField(help_text='Monto del plan', verbose_name='plan', max_digits=20, decimal_places=2, validators=[django.core.validators.MinValueValidator(1)])),
                ('destination', models.ForeignKey(related_name='plans', verbose_name='destino', to='core.Destination', help_text='Destino de gasto asociado')),
            ],
            options={
                'ordering': ('-year', 'destination'),
                'verbose_name': 'plan',
                'verbose_name_plural': 'planes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('yuid', models.PositiveIntegerField(help_text='Identificador \xfanico en el a\xf1o', verbose_name='registro', unique_for_year='date')),
                ('date', models.DateField(help_text='Fecha de emisi\xf3n', verbose_name='fecha')),
                ('amount', models.DecimalField(help_text='Importe de la entrada', verbose_name='importe', max_digits=20, decimal_places=2, validators=[django.core.validators.MinValueValidator(1)])),
                ('description', models.TextField(help_text='Descripci\xf3n de la entrada', verbose_name='descripci\xf3n', blank=True)),
                ('plan', models.PositiveIntegerField(default=2015, help_text='Plan anual asociado', verbose_name='plan', choices=[(2015, 2015), (2014, 2014)])),
                ('status', models.NullBooleanField(default=None, choices=[(None, 'Pendiente'), (True, 'Confirmado'), (False, 'Cancelado')], help_text='Estado del registro', verbose_name='estado')),
                ('concept', models.ForeignKey(related_name='records', verbose_name='concepto', to='core.Concept', help_text='Concepto por el cual se emite el registro')),
                ('destination', models.ForeignKey(related_name='records', verbose_name='destino', to='core.Destination', help_text='Destino de gasto asociado')),
            ],
            options={
                'verbose_name': 'registro',
                'verbose_name_plural': 'registros',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='plan',
            unique_together=set([('destination', 'year')]),
        ),
    ]
