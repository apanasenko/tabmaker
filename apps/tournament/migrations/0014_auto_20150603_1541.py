# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def add_access_messages(apps, schema_editor):
    Status = apps.get_model('tournament', 'TournamentStatus')
    status = [
        Status.objects.get(name='registration'),
        Status.objects.get(name='preparation'),
        Status.objects.get(name='started'),
        Status.objects.get(name='playoff'),
        Status.objects.get(name='finished'),
        ]

    Page = apps.get_model('tournament', 'Page')
    AccessToPage = apps.get_model('tournament', 'AccessToPage')
    messages = [None, None, None, None, None]

    page = Page.objects.get_or_create(name='remove')
    page[0].is_public = False
    page[0].save()
    for i in range(len(status)):
        access = AccessToPage.objects.get_or_create(
            page=page[0],
            status=status[i],
        )
        access[0].access = not messages[i]
        access[0].message = messages[i]
        access[0].message_ru = messages[i]
        access[0].save()


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0013_auto_20150603_0355'),
    ]

    operations = [
        migrations.RunPython(add_access_messages),
    ]
