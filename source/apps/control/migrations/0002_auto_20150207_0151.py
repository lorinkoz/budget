# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import common.validators


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='record',
            options={'ordering': ('-date', '-yuid'), 'verbose_name': 'registro', 'verbose_name_plural': 'registros'},
        ),
        migrations.AlterField(
            model_name='funding',
            name='amount',
            field=models.DecimalField(help_text='Importe de la entrada', verbose_name='importe', max_digits=20, decimal_places=2, validators=[common.validators.zero_validator]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='plan',
            name='amount',
            field=models.DecimalField(help_text='Monto del plan', verbose_name='plan', max_digits=20, decimal_places=2, validators=[common.validators.zero_validator]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='record',
            name='amount',
            field=models.DecimalField(help_text='Importe de la entrada', verbose_name='importe', max_digits=20, decimal_places=2, validators=[common.validators.zero_validator]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='record',
            name='plan',
            field=models.PositiveIntegerField(default=2015, help_text='Plan anual asociado', verbose_name='plan', choices=[(2015, 2015), (2014, 2014), (2013, 2013), (2012, 2012), (2011, 2011), (2010, 2010), (2009, 2009), (2008, 2008), (2007, 2007), (2006, 2006), (2005, 2005)]),
            preserve_default=True,
        ),
    ]
