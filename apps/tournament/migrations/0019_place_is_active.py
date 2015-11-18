# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0018_access_page__update_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
