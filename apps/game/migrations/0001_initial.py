# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('motion', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('date', models.DateTimeField()),
                ('Closing Government', models.ForeignKey(related_name='CG', to='team.Team')),
                ('Closing Opposition', models.ForeignKey(related_name='CO', to='team.Team')),
                ('Opening Government', models.ForeignKey(related_name='OG', to='team.Team')),
                ('Opening Opposition', models.ForeignKey(related_name='OO', to='team.Team')),
                ('chair', models.ForeignKey(related_name='chair', to=settings.AUTH_USER_MODEL)),
                ('motion', models.ForeignKey(to='motion.Motion')),
                ('wing_left', models.ForeignKey(related_name='wing_left', to=settings.AUTH_USER_MODEL)),
                ('wing_right', models.ForeignKey(related_name='wing_right', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GameResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('og', models.IntegerField()),
                ('oo', models.IntegerField()),
                ('cg', models.IntegerField()),
                ('co', models.IntegerField()),
                ('og_rev', models.BooleanField(default=False)),
                ('oo_rev', models.BooleanField(default=False)),
                ('cg_rev', models.BooleanField(default=False)),
                ('co_rev', models.BooleanField(default=False)),
                ('Prime Minister', models.IntegerField()),
                ('Deputy Prime Minister', models.IntegerField()),
                ('Leader of Opposition', models.IntegerField()),
                ('Deputy Leader of Opposition', models.IntegerField()),
                ('Member of Government', models.IntegerField()),
                ('Government Whip', models.IntegerField()),
                ('Member of Opposition', models.IntegerField()),
                ('Opposition Whip', models.IntegerField()),
                ('game', models.OneToOneField(to='game.Game')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
