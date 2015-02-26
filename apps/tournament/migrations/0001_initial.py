# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('motion', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('place', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('game', models.ForeignKey(to='game.Game')),
                ('place', models.ForeignKey(to='tournament.Place', on_delete=django.db.models.deletion.SET_NULL, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Round',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('number', models.IntegerField()),
                ('start_time', models.DateTimeField()),
                ('is_closed', models.BooleanField(default=False)),
                ('motion', models.ForeignKey(to='motion.Motion')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=100)),
                ('open_reg', models.DateTimeField(verbose_name='open registration')),
                ('close_reg', models.DateTimeField(verbose_name='close registration')),
                ('start_tour', models.DateTimeField(verbose_name='start tournament')),
                ('count_rounds', models.IntegerField()),
                ('is_closed', models.BooleanField(default=False)),
                ('info', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TournamentRole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('role', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserTournamentRel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('role', models.ForeignKey(to='tournament.TournamentRole')),
                ('tournament', models.ForeignKey(to='tournament.Tournament')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='tournament',
            name='members',
            field=models.ManyToManyField(through='tournament.UserTournamentRel', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='round',
            name='tournament',
            field=models.ForeignKey(to='tournament.Tournament'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='room',
            name='round',
            field=models.ForeignKey(to='tournament.Round'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='place',
            name='tournament',
            field=models.ForeignKey(to='tournament.Tournament'),
            preserve_default=True,
        ),
    ]
