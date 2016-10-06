# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import common.snippets.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='area',
            options={'ordering': ('code',), 'verbose_name': '\xe1rea', 'verbose_name_plural': '\xe1reas'},
        ),
        migrations.AlterModelOptions(
            name='concept',
            options={'ordering': ('code',), 'verbose_name': 'concepto', 'verbose_name_plural': 'conceptos'},
        ),
        migrations.AlterModelOptions(
            name='destination',
            options={'ordering': ('code',), 'verbose_name': 'destino de gasto', 'verbose_name_plural': 'destinos de gasto'},
        ),
        migrations.AlterModelOptions(
            name='element',
            options={'ordering': ('code',), 'verbose_name': 'elemento de gasto', 'verbose_name_plural': 'elementos de gasto'},
        ),
        migrations.AddField(
            model_name='area',
            name='slug',
            field=common.snippets.fields.AutoSlugField(editable=False, populate_from='name', allow_duplicates=False, separator='-', blank=True, verbose_name='slug', overwrite=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='area',
            name='code',
            field=models.CharField(help_text='C\xf3digo \xfanico asociado', max_length=10, verbose_name='c\xf3digo', validators=[django.core.validators.RegexValidator('^[\\w-]+$', 'El c\xf3digo solo puede tener letras o n\xfameros.')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='concept',
            name='code',
            field=models.CharField(help_text='C\xf3digo \xfanico asociado', max_length=10, verbose_name='c\xf3digo', validators=[django.core.validators.RegexValidator('^[\\w-]+$', 'El c\xf3digo solo puede tener letras o n\xfameros.')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='destination',
            name='code',
            field=models.CharField(help_text='C\xf3digo \xfanico asociado', max_length=10, verbose_name='c\xf3digo', validators=[django.core.validators.RegexValidator('^[\\w-]+$', 'El c\xf3digo solo puede tener letras o n\xfameros.')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='element',
            name='code',
            field=models.CharField(help_text='C\xf3digo \xfanico asociado', max_length=10, verbose_name='c\xf3digo', validators=[django.core.validators.RegexValidator('^[\\w-]+$', 'El c\xf3digo solo puede tener letras o n\xfameros.')]),
            preserve_default=True,
        ),
    ]
