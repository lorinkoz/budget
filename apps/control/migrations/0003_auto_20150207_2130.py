# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0002_auto_20150207_0151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, validators=[django.core.validators.MinValueValidator(0)], help_text='Monto del plan', verbose_name='plan'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='plan',
            name='year',
            field=models.PositiveIntegerField(default=2015, help_text='A\xf1o del plan', verbose_name='a\xf1o', choices=[(2015, 2015), (2014, 2014), (2013, 2013), (2012, 2012)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='record',
            name='plan',
            field=models.PositiveIntegerField(default=2015, help_text='Plan anual asociado', verbose_name='plan', choices=[(2015, 2015), (2014, 2014), (2013, 2013), (2012, 2012)]),
            preserve_default=True,
        ),
    ]
