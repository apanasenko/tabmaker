# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0016_access_page__update_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='round',
            name='is_public',
            field=models.BooleanField(default=True),
        ),
    ]
