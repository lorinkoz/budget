# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20180214_1344'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='default_currency',
            field=models.CharField(default='cup', max_length=3, verbose_name='moneda por defecto', choices=[('cup', 'CUP'), ('cuc', 'CUC')]),
            preserve_default=True,
        ),
    ]
