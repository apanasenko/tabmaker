# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0001_initial'),
        ('tournament', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamTournamentRel',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('role', models.ForeignKey(to='tournament.TournamentRole')),
                ('team', models.ForeignKey(to='team.Team')),
                ('tournament', models.ForeignKey(to='tournament.Tournament')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RenameField(
            model_name='tournament',
            old_name='members',
            new_name='user_members',
        ),
        migrations.AddField(
            model_name='tournament',
            name='team_members',
            field=models.ManyToManyField(to='team.Team', through='tournament.TeamTournamentRel'),
            preserve_default=True,
        ),
    ]
