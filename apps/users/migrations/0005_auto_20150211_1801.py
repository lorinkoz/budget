# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20150211_1758'),
    ]

    operations = [
        migrations.AlterField(
            model_name='areaauthority',
            name='area',
            field=models.ForeignKey(verbose_name='area', to='core.Area'),
            preserve_default=True,
        ),
    ]
