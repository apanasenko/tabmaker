# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0009_initial_page'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomFieldAlias',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='CustomFormType',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='CustomForm',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('form_type', models.ForeignKey(to='tournament.CustomFormType', on_delete=models.CASCADE)),
                ('tournament', models.ForeignKey(to='tournament.Tournament', on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='CustomFormAnswers',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('answers', models.TextField()),
                ('form', models.ForeignKey(to='tournament.CustomForm', on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='CustomQuestion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('question', models.CharField(max_length=300)),
                ('comment', models.TextField()),
                ('position', models.PositiveIntegerField()),
                ('required', models.BooleanField(default=True)),
                ('alias', models.ForeignKey(
                    blank=True,
                    to='tournament.CustomFieldAlias',
                    null=True,
                    on_delete=models.CASCADE
                )),
                ('form', models.ForeignKey(to='tournament.CustomForm', on_delete=models.CASCADE)),
            ],
        ),

    ]
