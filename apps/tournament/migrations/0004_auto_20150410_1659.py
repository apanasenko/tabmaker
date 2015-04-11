# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0003_auto_20150410_1557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='count_rounds',
            field=models.PositiveIntegerField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tournament',
            name='count_teams',
            field=models.PositiveIntegerField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tournament',
            name='count_teams_in_break',
            field=models.PositiveIntegerField(),
            preserve_default=True,
        ),
    ]
