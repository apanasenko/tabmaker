# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='wing_left',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='wing_left', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='game',
            name='wing_right',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='wing_right', null=True, blank=True),
            preserve_default=True,
        ),
    ]
