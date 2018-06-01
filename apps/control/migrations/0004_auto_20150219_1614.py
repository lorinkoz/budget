# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0003_auto_20150207_2130'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='funding',
            options={'ordering': ('-date', '-yuid'), 'verbose_name': 'asignaci\xf3n de fondos', 'verbose_name_plural': 'asignaciones de fondos'},
        ),
    ]
