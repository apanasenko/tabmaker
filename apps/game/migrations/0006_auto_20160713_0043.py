# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0005_add_fields__is_exist_speaker'),
        ('tournament', '0028_auto_20160712_2331'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='cg',
        ),
        migrations.RemoveField(
            model_name='game',
            name='chair',
        ),
        migrations.RemoveField(
            model_name='game',
            name='co',
        ),
        migrations.RemoveField(
            model_name='game',
            name='motion',
        ),
        migrations.RemoveField(
            model_name='game',
            name='og',
        ),
        migrations.RemoveField(
            model_name='game',
            name='oo',
        ),
        migrations.RemoveField(
            model_name='game',
            name='wing_left',
        ),
        migrations.RemoveField(
            model_name='game',
            name='wing_right',
        ),
        migrations.RemoveField(
            model_name='gameresult',
            name='game',
        ),
        migrations.DeleteModel(
            name='Game',
        ),
        migrations.DeleteModel(
            name='GameResult',
        ),
    ]
