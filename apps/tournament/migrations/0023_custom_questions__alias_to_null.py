# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0022_Custom_question__unique_keys'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customquestion',
            name='alias',
            field=models.ForeignKey(null=True, blank=True, to='tournament.CustomFieldAlias'),
        ),
    ]
