# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20150211_1801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='areaauthority',
            name='user',
            field=models.ForeignKey(verbose_name='usuario', to='users.User'),
            preserve_default=True,
        ),
    ]
