# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0014_auto_20150603_1541'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='location_lat',
            field=models.FloatField(default=131.89274039289919),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tournament',
            name='location_lon',
            field=models.FloatField(default=43.024658672481465),
            preserve_default=True,
        ),
    ]
