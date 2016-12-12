# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0014_change_profile_link_to_URL'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='adjudicator_experience',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='player_experience',
            field=models.TextField(blank=True),
        ),
    ]
