# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0004_auto_20150903_0430'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_show_email',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='user',
            name='is_show_phone',
            field=models.BooleanField(default=True),
        ),
    ]
