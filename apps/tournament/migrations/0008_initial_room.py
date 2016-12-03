# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0007_initial_round'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('number', models.IntegerField(blank=True)),
                ('game', models.ForeignKey(to='tournament.Game')),
                ('place', models.ForeignKey(
                    on_delete=django.db.models.deletion.SET_NULL,
                    blank=True,
                    to='tournament.Place',
                    null=True
                )),
                ('round', models.ForeignKey(to='tournament.Round')),
            ],
        ),
    ]
