# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-11 23:42
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
