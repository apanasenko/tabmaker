# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def add_pages(apps, schema_editor):
    Page = apps.get_model('tournament', 'Page')
    AccessToPage = apps.get_model('tournament', 'AccessToPage')
    Status = apps.get_model('tournament', 'TournamentStatus')

    # New page
    status = [
        Status.objects.get(name='registration'),
        Status.objects.get(name='preparation'),
        Status.objects.get(name='started'),
        Status.objects.get(name='playoff'),
        Status.objects.get(name='finished'),
    ]
    access_table = [
        [
            'custom_questions', False,
            None,
            None,
            None,
            None,
            None,
        ],
        [
            'custom_answers', False,
            None,
            None,
            None,
            None,
            None,
        ],
    ]
    for row in access_table:
        page = Page.objects.get_or_create(name=row[0], is_public=row[1])
        page[0].save()
        for i in range(len(row) - 2):
            access = AccessToPage.objects.get_or_create(
                page=page[0],
                status=status[i],
                access=(not row[i + 2]),
                message=row[i + 2],
                message_ru=row[i + 2]
            )
            access[0].save()



class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0031_gameresult2playoffresult'),
    ]

    operations = [
        migrations.RunPython(add_pages),
    ]
