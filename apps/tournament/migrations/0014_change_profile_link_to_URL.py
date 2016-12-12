# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0013_make_tournament_registration_hidden'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='link',
            field=models.URLField(blank=True, default='', max_length=100),
        ),
    ]
