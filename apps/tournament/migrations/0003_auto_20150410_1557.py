# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0002_auto_20150302_1230'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='count_teams',
            field=models.PositiveIntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tournament',
            name='count_teams_in_break',
            field=models.PositiveIntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tournament',
            name='link',
            field=models.URLField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tournament',
            name='count_rounds',
            field=models.PositiveIntegerField(default=0),
            preserve_default=True,
        ),
    ]
