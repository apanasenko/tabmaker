# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0017_botusers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='location',
            field=models.CharField(max_length=500),
        ),
    ]
