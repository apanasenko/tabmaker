# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models, connection


def move_sequence(apps, schema_editor):
    cursor = connection.cursor()
    for model in ['Game', 'GameResult', 'Team', 'Motion']:
        Model = apps.get_model('tournament', model)
        m = Model.objects.last()
        cursor.execute('ALTER SEQUENCE tournament_%s_id_seq RESTART WITH %d' % (model.lower(), m.id + 1))


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0028_auto_20160712_2331'),
    ]

    operations = [
        migrations.RunPython(move_sequence),
    ]
