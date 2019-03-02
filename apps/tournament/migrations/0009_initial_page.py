# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0008_initial_room'),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('is_public', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='AccessToPage',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('access', models.BooleanField(default=True)),
                ('message', models.TextField(blank=True, null=True)),
                ('message_ru', models.TextField(blank=True, null=True)),
                ('message_en', models.TextField(blank=True, null=True)),
                ('page', models.ForeignKey(to='tournament.Page', on_delete=models.CASCADE)),
                ('status', models.ForeignKey(to='tournament.TournamentStatus', on_delete=models.CASCADE)),
            ],
        ),
    ]
