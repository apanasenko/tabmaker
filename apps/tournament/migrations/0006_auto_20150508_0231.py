# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def generate_tournament_status(apps, schema_editor):
    TournamentStatus = apps.get_model('tournament', 'TournamentStatus')
    names = [
        'registration',
        'preparation',
        'started',
        'finished'
    ]

    for name in names:
        status = TournamentStatus.objects.create(name=name)
        status.save()


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0005_auto_20150508_0228'),
    ]

    operations = [
        migrations.RunPython(generate_tournament_status),
    ]
