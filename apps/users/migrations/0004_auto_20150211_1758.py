# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20150211_1758'),
        ('users', '0003_auto_20150207_2251'),
    ]

    operations = [
        migrations.CreateModel(
            name='AreaAuthority',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('can_modify', models.BooleanField(default=False, verbose_name='permiso', choices=[(True, 'Consultar y modificar'), (False, 'Solo consultar')])),
                ('area', models.ForeignKey(verbose_name='areas autorizadas', blank=True, to='core.Area', null=True)),
                ('user', models.OneToOneField(verbose_name='usuario', to='users.User')),
            ],
            options={
                'verbose_name': 'autoridad sobre \xe1rea',
                'verbose_name_plural': 'autoridad sobre \xe1reas',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='areaauthority',
            unique_together=set([('user', 'area')]),
        ),
        migrations.AddField(
            model_name='user',
            name='areas',
            field=models.ManyToManyField(to='core.Area', verbose_name='areas autorizadas', through='users.AreaAuthority'),
            preserve_default=True,
        ),
    ]
