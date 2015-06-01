# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def add_translation_to_role(apps, schema_editor):
    TournamentRole = apps.get_model('tournament', 'TournamentRole')
    roles = [
        ['owner', 'Владелец', 'Owner'],
        ['admin', 'Администратор', 'Admin'],
        ['registered', 'Зарегистрированный', 'Registered'],
        ['in_tab', 'В тэбе', 'In tab'],
        ['wait_list', 'Вейт-лист', 'Wait list'],
        ['verified', 'Команда подтвердила', 'Verified'],
        ['approved', 'Организатор подтвердил', 'Approved'],
        ['member', 'Участник', 'Member'],
        ['registered_adjudicator', 'Зарегистрирован как судья', 'Registered adjudicator'],
        ['approved_adjudicator', 'Судья в списке', 'Approved adjudicator'],
        ['chair', 'Судья', 'Chair'],
        ['wing', 'Боковой судья', 'Wing'],
        ['chief_adjudicator', 'Главный судья (турнира)', 'Chief adjudicator'],
    ]

    for role in roles:
        role_obj = TournamentRole.objects.get_or_create(role=role[0])
        role_obj[0].role_en = role[2]
        role_obj[0].role_ru = role[1]
        role_obj[0].save()


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0009_auto_20150523_1242'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournamentrole',
            name='role_en',
            field=models.CharField(null=True, max_length=100),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tournamentrole',
            name='role_ru',
            field=models.CharField(null=True, max_length=100),
            preserve_default=True,
        ),
        migrations.RunPython(add_translation_to_role),
    ]
