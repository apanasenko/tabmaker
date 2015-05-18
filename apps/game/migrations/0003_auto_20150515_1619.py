# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_auto_20150226_1648'),
    ]

    operations = [
        migrations.RenameField(
            model_name='game',
            old_name='Closing Government',
            new_name='cg',
        ),
        migrations.RenameField(
            model_name='game',
            old_name='Closing Opposition',
            new_name='co',
        ),
        migrations.RenameField(
            model_name='game',
            old_name='Opening Government',
            new_name='og',
        ),
        migrations.RenameField(
            model_name='game',
            old_name='Opening Opposition',
            new_name='oo',
        ),
    ]
