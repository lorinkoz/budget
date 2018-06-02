# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0005_auto_20180214_1344'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='month',
            field=models.PositiveIntegerField(default=1, help_text='Mes del plan', verbose_name='mes', choices=[(1, 'Enero'), (2, 'Febrero'), (3, 'Marzo'), (4, 'Abril'), (5, 'Mayo'), (6, 'Junio'), (7, 'Julio'), (8, 'Agosto'), (9, 'Septiembre'), (10, 'Octubre'), (11, 'Noviembre'), (12, 'Diciembre')]),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='plan',
            unique_together=set([('destination', 'year', 'month')]),
        ),
    ]
