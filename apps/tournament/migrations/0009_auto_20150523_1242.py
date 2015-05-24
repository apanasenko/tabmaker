# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def add_tournament_status(apps, schema_editor):
    TournamentStatus = apps.get_model('tournament', 'TournamentStatus')

    status = TournamentStatus.objects.create(name='playoff')
    status.save()


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0008_auto_20150519_0040'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='number',
            field=models.IntegerField(default=0, blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='round',
            name='is_playoff',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.RunPython(add_tournament_status),
    ]
