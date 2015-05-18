# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def generate_tournament_role(apps, schema_editor):
    TournamentRole = apps.get_model('tournament', 'TournamentRole')
    roles = [
        'owner',
        'admin',
        'registered',
        'in_tab',
        'wait_list',
        'verified',
        'approved',
        'member',
        'registered_adjudicator',
        'approved_adjudicator',
        'chair',
        'wing',
        'chief_adjudicator',
    ]

    for role in roles:
        role_obj = TournamentRole.objects.get_or_create(role=role)
        role_obj[0].save()


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0007_tournament_cur_round'),
    ]

    operations = [
        migrations.RunPython(generate_tournament_role),
    ]
