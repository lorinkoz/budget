# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_display_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.PositiveIntegerField(default=0, verbose_name='rol', choices=[(0, 'Inactivo'), (1, 'Consultor'), (2, 'Operador'), (3, 'Administrador')]),
            preserve_default=True,
        ),
    ]
