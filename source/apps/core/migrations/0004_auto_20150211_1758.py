# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_remove_element_creditable'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='area',
            options={'ordering': ('code', 'name'), 'verbose_name': '\xe1rea', 'verbose_name_plural': '\xe1reas'},
        ),
        migrations.AlterModelOptions(
            name='concept',
            options={'ordering': ('code', 'name'), 'verbose_name': 'concepto', 'verbose_name_plural': 'conceptos'},
        ),
        migrations.AlterModelOptions(
            name='destination',
            options={'ordering': ('code', 'name'), 'verbose_name': 'destino de gasto', 'verbose_name_plural': 'destinos de gasto'},
        ),
        migrations.AlterModelOptions(
            name='element',
            options={'ordering': ('code', 'name'), 'verbose_name': 'elemento de gasto', 'verbose_name_plural': 'elementos de gasto'},
        ),
    ]
