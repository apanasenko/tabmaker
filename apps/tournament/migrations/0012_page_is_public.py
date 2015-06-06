# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def set_public_field(apps, schema_editor):
    Page = apps.get_model('tournament', 'Page')
    is_public = [
        ['show', True],
        ['edit', False],
        ['play', False],
        ['break', False],
        ['result', True],
        ['round_next', False],
        ['round_edit', False],
        ['round_result', False],
        ['round_remove', False],
        ['team/adju. list', True],
        ['team/adju. edit', False],
        ['team/adju. registration', True],
        ['registration_action', False],
        ]

    for i in is_public:
        page = Page.objects.filter(name=i[0]).update(is_public=i[1])


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0011_auto_20150601_1921'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='is_public',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.RunPython(set_public_field),
    ]
