# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0012_fix_username_length'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='is_registration_hidden',
            field=models.BooleanField(default=False),
        ),
    ]
