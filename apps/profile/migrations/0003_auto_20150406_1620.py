# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0002_auto_20150405_1637'),
    ]

    operations = [
        migrations.RenameField(
            model_name='university',
            old_name='city_id',
            new_name='city',
        ),
        migrations.RenameField(
            model_name='university',
            old_name='country_id',
            new_name='country',
        ),
        migrations.RemoveField(
            model_name='user',
            name='city_vk_id',
        ),
        migrations.RemoveField(
            model_name='user',
            name='country_vk_id',
        ),
        migrations.RemoveField(
            model_name='user',
            name='university_vk_id',
        ),
        migrations.AddField(
            model_name='user',
            name='university',
            field=models.ForeignKey(to='profile.University', null=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='university',
            unique_together=set([('country', 'city', 'university_id')]),
        ),
    ]
