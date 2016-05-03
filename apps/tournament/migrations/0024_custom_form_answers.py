# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0023_custom_questions__alias_to_null'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomFormAnswers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('answers', models.TextField()),
                ('form', models.ForeignKey(to='tournament.CustomForm')),
            ],
        ),
    ]
