# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def remove_pages(apps, schema_editor):
    Page = apps.get_model('tournament', 'Page')
    AccessToPage = apps.get_model('tournament', 'AccessToPage')
    Status = apps.get_model('tournament', 'TournamentStatus')

    # Remove unused
    Page.objects.filter(name='registration_action').delete()
    Page.objects.filter(name='team/adju. list').delete()

    # Update
    Page.objects.filter(name='round_result').update(is_public=True)

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
            'registration opening', False,
            'Регистрация уже открыта',
            None,
            'Для открытия регистрации необходимо отменить старт турнира',
            'Для открытия регистрации необходимо отменить старт турнира',
            'Невозможно открыть регистрацию в завершённом турнире'
        ],
        [
            'registration closing', False,
            None,
            'Регистрация уже закрыта',
            None,
            'Для отмены старта турнира необходимо отменить брейк',
            'Невозможно отменить старт турнира, когда он завершился'
        ],
        [
            'start', False,
            'Для старта турнира необходимо закрыть регистрацию',
            None,
            'Турнир уже идёт',
            None,
            'Турнир уже завершён'
        ],
        [
            'round_show', True,
            'К сожалению, раунд ещё не объявлен',
            'К сожалению, раунд ещё не объявлен',
            None,
            None,
            'Турнир уже завершён'
        ],
        [
            'team/adju. add', False,
            None,
            None,
            None,
            None,
            'Турнир уже завершён'
        ]
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
        ('tournament', '0015_auto_20150612_1728'),
    ]

    operations = [
        migrations.RunPython(remove_pages),
    ]
