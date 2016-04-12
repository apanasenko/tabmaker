# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def add_custom_forms_types(apps, schema_editor):
    CustomFormType = apps.get_model('tournament', 'CustomFormType')
    types = [
        'registration',
        'feedback',
    ]

    for type_name in types:
        status_obj = CustomFormType.objects.get_or_create(name=type_name)
        status_obj[0].save()


def add_custom_fields_alias(apps, schema_editor):
    CustomFieldAlias = apps.get_model('tournament', 'CustomFieldAlias')
    aliases = [
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
    ]

    for alias in aliases:
        status_obj = CustomFieldAlias.objects.get_or_create(name=alias)
        status_obj[0].save()


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0020_tournament_status__translate_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomFieldAlias',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='CustomFormType',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='CustomForm',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('tournament', models.OneToOneField(to='tournament.Tournament')),
                ('link', models.TextField(default='')),
                ('form_type', models.ForeignKey(to='tournament.CustomFormType')),
            ],
        ),
        migrations.CreateModel(
            name='CustomQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('question', models.CharField(max_length=300)),
                ('comment', models.TextField()),
                ('position', models.PositiveIntegerField(unique=True)),
                ('required', models.BooleanField(default=True)),
                ('form', models.ForeignKey(to='tournament.CustomForm')),
                ('alias', models.ForeignKey(blank=True, to='tournament.CustomFieldAlias', )),
            ],
        ),
        migrations.RunPython(add_custom_forms_types),
        migrations.RunPython(add_custom_fields_alias),
    ]
