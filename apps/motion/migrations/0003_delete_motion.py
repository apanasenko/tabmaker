# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0028_auto_20160712_2331'),
        ('game', '0006_auto_20160713_0043'),
        ('motion', '0002_motion_infoslide'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Motion',
        ),
    ]
