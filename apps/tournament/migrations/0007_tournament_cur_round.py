# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0006_auto_20150508_0231'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='cur_round',
            field=models.PositiveIntegerField(default=0),
            preserve_default=True,
        ),
    ]
