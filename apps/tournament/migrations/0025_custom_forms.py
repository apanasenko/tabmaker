# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def add_custom_forms_types(apps, schema_editor):
    CustomFormType = apps.get_model('tournament', 'CustomFormType')
    types = [
        'adjudicator',
        'audience',
    ]

    CustomFormType.objects.filter(name='registration').update(name='teams')
    for type_name in types:
        status_obj = CustomFormType.objects.get_or_create(name=type_name)
        status_obj[0].save()


def add_custom_fields_alias(apps, schema_editor):
    CustomFieldAlias = apps.get_model('tournament', 'CustomFieldAlias')
    aliases = [
        'adjudicator',
    ]

    for alias in aliases:
        status_obj = CustomFieldAlias.objects.get_or_create(name=alias)
        status_obj[0].save()


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0024_custom_form_answers'),
    ]

    operations = [
        migrations.RunPython(add_custom_forms_types),
        migrations.RunPython(add_custom_fields_alias),
    ]
