# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0006_initial_place'),
    ]

    operations = [
        migrations.CreateModel(
            name='Round',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('number', models.IntegerField()),
                ('start_time', models.DateTimeField()),
                ('is_closed', models.BooleanField(default=False)),
                ('is_public', models.BooleanField(default=True)),
                ('is_playoff', models.BooleanField(default=False)),
                ('motion', models.ForeignKey(to='tournament.Motion')),
                ('tournament', models.ForeignKey(to='tournament.Tournament')),
            ],
        ),
    ]
