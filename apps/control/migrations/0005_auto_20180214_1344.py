# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0004_auto_20150219_1614'),
    ]

    operations = [
        migrations.AddField(
            model_name='funding',
            name='currency',
            field=models.CharField(default='cup', help_text='Moneda de la entrada', max_length=3, verbose_name='moneda', choices=[('cup', 'CUP'), ('cuc', 'CUC')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='record',
            name='currency',
            field=models.CharField(default='cup', help_text='Moneda de la entrada', max_length=3, verbose_name='moneda', choices=[('cup', 'CUP'), ('cuc', 'CUC')]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='plan',
            name='year',
            field=models.PositiveIntegerField(default=2018, help_text='A\xf1o del plan', verbose_name='a\xf1o', choices=[(2018, 2018), (2017, 2017), (2016, 2016), (2015, 2015), (2014, 2014), (2013, 2013), (2012, 2012)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='record',
            name='plan',
            field=models.PositiveIntegerField(default=2018, help_text='Plan anual asociado', verbose_name='plan', choices=[(2018, 2018), (2017, 2017), (2016, 2016), (2015, 2015), (2014, 2014), (2013, 2013), (2012, 2012)]),
            preserve_default=True,
        ),
    ]
