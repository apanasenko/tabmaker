# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0026_remove_customform_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customform',
            name='tournament',
            field=models.ForeignKey(to='tournament.Tournament'),
        ),
    ]
