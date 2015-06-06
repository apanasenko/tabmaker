# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def create_access_messages(apps, schema_editor):
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
    access_table = [
        ['show', None, None, None, None, None],
        ['edit', None, None, None, None, 'Турнир уже завершён, вы не можете вносить изменения'],
        [
            'play',
            'Эта страница станет доступной после начала турнира',
            'Эта страница станет доступной после начала турнира',
            None,
            None,
            'Турнир уже завершён, вы не можете вносить изменения'
        ],
        [
            'break',
            'Вы не можете объявить брейк до начала турнира',
            'Вы не можете объявить брейк до начала турнира',
            None,
            'Брейк уже объявлен',
            'Турнир уже завершён, вы не можете объявить брейк'
        ],
        [
            'result',
            'Ещё нет сыгранных раундов',
            'Ещё нет сыгранных раундов',
            None,
            None,
            None
        ],
        [
            'round_next',
            'Для создания раунда необходимо начать турнир',
            'Для создания раунда необходимо начать турнир',
            None,
            None,
            'Турнир уже завершён, вы не можете создавать новые раунды'
        ],
        [
            'round_edit',
            'Турнир ещё не начался, вы не можете редактировать раунды',
            'Турнир ещё не начался, вы не можете редактировать раунды',
            None,
            None,
            'Вы не можете редактировать раунды в завершённом турнире'
        ],
        [
            'round_result',
            'Турнир ещё не начался, нет сыгранных раундов',
            'Турнир ещё не начался, нет сыгранных раундов',
            None,
            None,
            'Вы не можете исправлять результаты в завершённом турнире'
        ],
        [
            'round_remove',
            'Турнир ещё не начался, нет созданных раундов',
            'Турнир ещё не начался, нет созданных раундов',
            None,
            None,
            'Вы не можете удалить раунд в завершённом турнире'
        ],
        ['team/adju. list', None, None, None, None, None],
        ['team/adju. edit', None, None, None, None, 'Турнир уже завершён, вы не можете сменить статус участников'],
        [
            'team/adju. registration',
            None,
            'Регистрация уже завершена. Обратитесь к организаторам турнира',
            'Турнир уже стартовал. Для внесения каких либо изменений обратитесь к организаторам турнира',
            'Турнир уже стартовал. Для внесения каких либо изменений обратитесь к организаторам турнира',
            'Вы не можете регистрироваться в завершённый турнир'],
        [
            'registration_action',
            None,
            None,
            'Турнир уже идёт',
            'Турнир уже идёт',
            'Турнир уже завершился'
        ],
    ]

    for row in access_table:
        page = Page.objects.get_or_create(name=row[0])
        page[0].save()
        for i in range(len(row) - 1):
            access = AccessToPage.objects.get_or_create(
                page=page[0],
                status=status[i],
                access=(not row[i + 1]),
                message=row[i + 1],
                message_ru=row[i + 1]
            )
            access[0].save()


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0010_auto_20150601_0309'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessToPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access', models.BooleanField(default=True)),
                ('message', models.TextField(null=True, blank=True)),
                ('message_ru', models.TextField(null=True, blank=True)),
                ('message_en', models.TextField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='accesstopage',
            name='page',
            field=models.ForeignKey(to='tournament.Page'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='accesstopage',
            name='status',
            field=models.ForeignKey(to='tournament.TournamentStatus'),
            preserve_default=True,
        ),
        migrations.RunPython(create_access_messages),
    ]
