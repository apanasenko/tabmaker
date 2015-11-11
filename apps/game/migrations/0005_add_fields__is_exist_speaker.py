# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0004_auto_20150518_1654'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameresult',
            name='dlo_exist',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='gameresult',
            name='dpm_exist',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='gameresult',
            name='gw_exist',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='gameresult',
            name='lo_exist',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='gameresult',
            name='mg_exist',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='gameresult',
            name='mo_exist',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='gameresult',
            name='ow_exist',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='gameresult',
            name='pm_exist',
            field=models.BooleanField(default=True),
        ),
    ]
