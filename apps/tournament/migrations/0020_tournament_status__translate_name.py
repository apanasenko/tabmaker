# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def add_translation_to_status(apps, schema_editor):
    TournamentStatus = apps.get_model('tournament', 'TournamentStatus')
    statuses = [
        ['registration', 'Регистрация открыта', 'Registration open'],
        ['preparation', 'Регистрация закрыта', 'Registration closed'],
        ['started', 'Отборочные раунды', 'Qualification'],
        ['playoff', 'Плейофф', 'Playoff'],
        ['finished', 'Окончен', 'Finished'],
    ]

    for status in statuses:
        status_obj = TournamentStatus.objects.get_or_create(name=status[0])
        status_obj[0].name_ru = status[1]
        status_obj[0].name_en = status[2]
        status_obj[0].save()


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0019_place_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournamentstatus',
            name='name_en',
            field=models.CharField(null=True, max_length=100),
        ),
        migrations.AddField(
            model_name='tournamentstatus',
            name='name_ru',
            field=models.CharField(null=True, max_length=100),
        ),
        migrations.RunPython(add_translation_to_status)
    ]
