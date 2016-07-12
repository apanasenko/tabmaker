# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models, connection
from django.conf import settings


def copy_tables(apps, schema_editor):
    cursor = connection.cursor()
    cursor.execute('INSERT INTO tournament_motion SELECT * FROM motion_motion')
    cursor.execute('INSERT INTO tournament_team SELECT * FROM team_team')

    Game = apps.get_model('tournament', 'Game')
    for game in Game.objects.raw('SELECT * FROM game_game'):
        game.save()

    GameResult = apps.get_model('tournament', 'GameResult')
    for game in GameResult.objects.raw('SELECT * FROM game_gameresult'):
        game.save()

    # cursor.execute('INSERT INTO tournament_game SELECT * FROM game_game')
    # cursor.execute('INSERT INTO tournament_gameresult SELECT * FROM game_gameresult')


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tournament', '0027_alter_custom_form'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='GameResult',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('og', models.IntegerField()),
                ('oo', models.IntegerField()),
                ('cg', models.IntegerField()),
                ('co', models.IntegerField()),
                ('og_rev', models.BooleanField(default=False)),
                ('oo_rev', models.BooleanField(default=False)),
                ('cg_rev', models.BooleanField(default=False)),
                ('co_rev', models.BooleanField(default=False)),
                ('pm', models.IntegerField()),
                ('pm_exist', models.BooleanField(default=True)),
                ('dpm', models.IntegerField()),
                ('dpm_exist', models.BooleanField(default=True)),
                ('lo', models.IntegerField()),
                ('lo_exist', models.BooleanField(default=True)),
                ('dlo', models.IntegerField()),
                ('dlo_exist', models.BooleanField(default=True)),
                ('mg', models.IntegerField()),
                ('mg_exist', models.BooleanField(default=True)),
                ('gw', models.IntegerField()),
                ('gw_exist', models.BooleanField(default=True)),
                ('mo', models.IntegerField()),
                ('mo_exist', models.BooleanField(default=True)),
                ('ow', models.IntegerField()),
                ('ow_exist', models.BooleanField(default=True)),
                ('game', models.OneToOneField(to='tournament.Game')),
            ],
        ),
        migrations.CreateModel(
            name='Motion',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('motion', models.TextField()),
                ('infoslide', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('info', models.TextField(blank=True)),
                ('speaker_1', models.ForeignKey(related_name='first_speaker', to=settings.AUTH_USER_MODEL)),
                ('speaker_2', models.ForeignKey(related_name='second_speaker', to=settings.AUTH_USER_MODEL)),
            ],
        ),

        migrations.AddField(
            model_name='game',
            name='cg',
            field=models.ForeignKey(related_name='CG', to='tournament.Team'),
        ),
        migrations.AddField(
            model_name='game',
            name='chair',
            field=models.ForeignKey(related_name='chair', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='game',
            name='co',
            field=models.ForeignKey(related_name='CO', to='tournament.Team'),
        ),
        migrations.AddField(
            model_name='game',
            name='motion',
            field=models.ForeignKey(to='tournament.Motion'),
        ),
        migrations.AddField(
            model_name='game',
            name='og',
            field=models.ForeignKey(related_name='OG', to='tournament.Team'),
        ),
        migrations.AddField(
            model_name='game',
            name='oo',
            field=models.ForeignKey(related_name='OO', to='tournament.Team'),
        ),
        migrations.AddField(
            model_name='game',
            name='wing_left',
            field=models.ForeignKey(blank=True, related_name='wing_left', null=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='game',
            name='wing_right',
            field=models.ForeignKey(blank=True, related_name='wing_right', null=True, to=settings.AUTH_USER_MODEL),
        ),

        migrations.RunPython(copy_tables),

        migrations.AlterField(
            model_name='room',
            name='game',
            field=models.ForeignKey(to='tournament.Game'),
        ),
        migrations.AlterField(
            model_name='round',
            name='motion',
            field=models.ForeignKey(to='tournament.Motion'),
        ),
        migrations.AlterField(
            model_name='teamtournamentrel',
            name='team',
            field=models.ForeignKey(to='tournament.Team'),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='team_members',
            field=models.ManyToManyField(through='tournament.TeamTournamentRel', to='tournament.Team'),
        ),
    ]
