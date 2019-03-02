# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0004_initial_game'),
    ]

    operations = [
        migrations.CreateModel(
            name='TournamentRole',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('role', models.CharField(max_length=100)),
                ('role_ru', models.CharField(max_length=100, null=True)),
                ('role_en', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TournamentStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('name_ru', models.CharField(max_length=100, null=True)),
                ('name_en', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=100)),
                ('location_lon', models.FloatField(default=43.024658672481465)),
                ('location_lat', models.FloatField(default=131.89274039289919)),
                ('open_reg', models.DateTimeField(verbose_name='open registration')),
                ('close_reg', models.DateTimeField(verbose_name='close registration')),
                ('start_tour', models.DateTimeField(verbose_name='start tournament')),
                ('count_rounds', models.PositiveIntegerField()),
                ('count_teams', models.PositiveIntegerField()),
                ('count_teams_in_break', models.PositiveIntegerField()),
                ('link', models.URLField(blank=True, null=True)),
                ('cur_round', models.PositiveIntegerField(default=0)),
                ('info', models.TextField()),
                ('status', models.ForeignKey(null=True, to='tournament.TournamentStatus', on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='UserTournamentRel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('role', models.ForeignKey(to='tournament.TournamentRole', on_delete=models.CASCADE)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
                ('tournament', models.ForeignKey(to='tournament.Tournament', on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='TeamTournamentRel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('role', models.ForeignKey(to='tournament.TournamentRole', on_delete=models.CASCADE)),
                ('team', models.ForeignKey(to='tournament.Team', on_delete=models.CASCADE)),
                ('tournament', models.ForeignKey(to='tournament.Tournament', on_delete=models.CASCADE)),
            ],
        ),

        migrations.AddField(
            model_name='tournament',
            name='team_members',
            field=models.ManyToManyField(through='tournament.TeamTournamentRel', to='tournament.Team'),
        ),
        migrations.AddField(
            model_name='tournament',
            name='user_members',
            field=models.ManyToManyField(through='tournament.UserTournamentRel', to=settings.AUTH_USER_MODEL),
        ),
    ]
