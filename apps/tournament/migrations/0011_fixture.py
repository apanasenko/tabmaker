# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import migrations


def generate_tournament_statuses(apps, schema_editor):
    TournamentStatus = apps.get_model('tournament', 'TournamentStatus')

    tournament_statuses = [
        ['registration', 'Регистрация открыта', 'Registration open'],
        ['preparation', 'Регистрация закрыта', 'Registration closed'],
        ['started', 'Отборочные раунды', 'Qualification'],
        ['playoff', 'Плейофф', 'Playoff'],
        ['finished', 'Окончен', 'Finished'],
    ]

    for tournament_status in tournament_statuses:
        status = TournamentStatus.objects.get_or_create(name=tournament_status[0])
        status[0].name_ru = tournament_status[1]
        status[0].name_en = tournament_status[2]
        status[0].save()


def generate_tournament_roles(apps, schema_editor):
    TournamentRole = apps.get_model('tournament', 'TournamentRole')

    tournament_roles = [
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

    for tournament_role in tournament_roles:
        role = TournamentRole.objects.get_or_create(role=tournament_role[0])
        role[0].role_en = tournament_role[2]
        role[0].role_ru = tournament_role[1]
        role[0].save()


def generate_privileges_for_access_page(apps, schema_editor):
    Page = apps.get_model('tournament', 'Page')
    AccessToPage = apps.get_model('tournament', 'AccessToPage')
    TournamentStatus = apps.get_model('tournament', 'TournamentStatus')

    tournament_statuses = [
        TournamentStatus.objects.get(name='registration'),
        TournamentStatus.objects.get(name='preparation'),
        TournamentStatus.objects.get(name='started'),
        TournamentStatus.objects.get(name='playoff'),
        TournamentStatus.objects.get(name='finished'),
    ]

    access_table = [
        # [name_page, is_public, registration_message, preparation_message, ...]
        ['show', True, None, None, None, None, None],
        ['edit', False, None, None, None, None, 'Турнир уже завершён, вы не можете вносить изменения'],
        ['remove', False, None, None, None, None, None],
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
            'break', False,
            'Вы не можете объявить брейк до начала турнира',
            'Вы не можете объявить брейк до начала турнира',
            None,
            'Брейк уже объявлен',
            'Турнир уже завершён, вы не можете объявить брейк'
        ],
        [
            'finished', False,
            'Вы не можете завершить турнир, который ещё не начался',
            'Вы не можете завершить турнир, который ещё не начался',
            None,
            None,
            'Турнир уже завершён'
        ],
        [
            'team/adju. registration', True,
            None,
            'Регистрация уже завершена. Обратитесь к организаторам турнира',
            'Турнир уже стартовал. Для внесения каких либо изменений обратитесь к организаторам турнира',
            'Турнир уже стартовал. Для внесения каких либо изменений обратитесь к организаторам турнира',
            'Вы не можете регистрироваться в завершённый турнир'
        ],
        [
            'team/adju. add', False,
            None,
            None,
            None,
            None,
            'Турнир уже завершён'
        ],
        [
            'team/adju. edit', False,
            None,
            None,
            None,
            None,
            'Турнир уже завершён, вы не можете сменить статус участников'
        ],
        # not used
        ['admin edit', False, None, None, None, None, 'Турнир уже завершён'],
        ['print', False, None, None, None, None, None],
        [
            'play', False,
            'Эта страница станет доступной после начала турнира',
            'Эта страница станет доступной после начала турнира',
            None,
            None,
            'Турнир уже завершён, вы не можете вносить изменения'
        ],
        [
            'round_next', False,
            'Для создания раунда необходимо начать турнир',
            'Для создания раунда необходимо начать турнир',
            None,
            None,
            'Турнир уже завершён, вы не можете создавать новые раунды'
        ],
        [
            'round_edit', False,
            'Турнир ещё не начался, вы не можете редактировать раунды',
            'Турнир ещё не начался, вы не можете редактировать раунды',
            None,
            None,
            'Вы не можете редактировать раунды в завершённом турнире'
        ],
        [
            'round publish', False,
            'Для публикации раунда необходимо начать турнир и создать раунд',
            'Для публикации раунда необходимо начать турнир и создать раунд',
            None,
            None,
            'Турнир уже завершён',
        ],
        [
            'round presentation', False,
            'Для создания презентации необходимо начать турнир и создать раунд',
            'Для создания презентации необходимо начать турнир и создать раунд',
            None,
            None,
            'Турнир уже завершён',
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
            'round_result', True,
            'Турнир ещё не начался, нет сыгранных раундов',
            'Турнир ещё не начался, нет сыгранных раундов',
            None,
            None,
            'Вы не можете исправлять результаты в завершённом турнире'
        ],
        [
            'round_remove', False,
            'Турнир ещё не начался, нет созданных раундов',
            'Турнир ещё не начался, нет созданных раундов',
            None,
            None,
            'Вы не можете удалить раунд в завершённом турнире'
        ],
        [
            'result', True,
            'Ещё нет сыгранных раундов',
            'Ещё нет сыгранных раундов',
            None,
            None,
            None
        ],
        [
            'result_all', True,
            'Нет сыгранных раундов',
            'Нет сыгранных раундов',
            None,
            None,
            None,
        ],
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
        page = Page.objects.get_or_create(name=row[0])
        page[0].is_public = row[1]
        page[0].save()
        for i in range(len(row) - 2):
            access = AccessToPage.objects.get_or_create(page=page[0], status=tournament_statuses[i])
            access[0].access = (not row[i + 2])
            access[0].message = row[i + 2]
            access[0].message_ru = row[i + 2]
            access[0].save()


def generate_custom_forms_types(apps, schema_editor):
    CustomFormType = apps.get_model('tournament', 'CustomFormType')

    custom_form_types = [
        'registration',
        'feedback',
        'adjudicator',
        'audience',
    ]

    for type_name in custom_form_types:
        custom_form_type = CustomFormType.objects.get_or_create(name=type_name)
        custom_form_type[0].save()


def generate_custom_fields_alias(apps, schema_editor):
    CustomFieldAlias = apps.get_model('tournament', 'CustomFieldAlias')

    custom_field_aliases = [
        'name',
        'speaker_1_email',
        'speaker_1_first_name',
        'speaker_1_last_name',
        'speaker_1_university',
        'speaker_2_email',
        'speaker_2_first_name',
        'speaker_2_last_name',
        'speaker_2_university',
        'team_name',
        'adjudicator',
    ]

    for alias_name in custom_field_aliases:
        custom_field_alias = CustomFieldAlias.objects.get_or_create(name=alias_name)
        custom_field_alias[0].save()


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0010_initial_custom_forms'),
    ]

    operations = [
        migrations.RunPython(generate_tournament_statuses),
        migrations.RunPython(generate_tournament_roles),
        migrations.RunPython(generate_privileges_for_access_page),
        migrations.RunPython(generate_custom_forms_types),
        migrations.RunPython(generate_custom_fields_alias),
    ]
