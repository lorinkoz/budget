# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20150207_2130'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='element',
            name='creditable',
        ),
    ]
