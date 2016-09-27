# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0028_auto_20160712_2331'),
        ('game', '0006_auto_20160713_0043'),
        ('team', '0002_Team__info_to_blank'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='speaker_1',
        ),
        migrations.RemoveField(
            model_name='team',
            name='speaker_2',
        ),
        migrations.DeleteModel(
            name='Team',
        ),
    ]
