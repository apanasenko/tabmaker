# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0021_custom_forms'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customquestion',
            name='position',
            field=models.PositiveIntegerField(),
        ),
    ]
