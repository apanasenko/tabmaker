# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0003_initial_team'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('date', models.DateTimeField()),
                ('motion', models.ForeignKey(to='tournament.Motion', on_delete=models.CASCADE)),
                ('og', models.ForeignKey(related_name='OG', to='tournament.Team', on_delete=models.CASCADE)),
                ('oo', models.ForeignKey(related_name='OO', to='tournament.Team', on_delete=models.CASCADE)),
                ('cg', models.ForeignKey(related_name='CG', to='tournament.Team', on_delete=models.CASCADE)),
                ('co', models.ForeignKey(related_name='CO', to='tournament.Team', on_delete=models.CASCADE)),
                ('chair', models.ForeignKey(
                    related_name='chair',
                    to=settings.AUTH_USER_MODEL,
                    on_delete=models.CASCADE
                )),
                ('wing_left', models.ForeignKey(
                    related_name='wing_left',
                    null=True,
                    to=settings.AUTH_USER_MODEL,
                    blank=True,
                    on_delete=models.CASCADE
                )),
                ('wing_right', models.ForeignKey(
                    related_name='wing_right',
                    null=True,
                    to=settings.AUTH_USER_MODEL,
                    blank=True,
                    on_delete=models.CASCADE
                )),
            ],
        ),
        migrations.CreateModel(
            name='GameResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('og_rev', models.BooleanField(default=False)),
                ('oo_rev', models.BooleanField(default=False)),
                ('cg_rev', models.BooleanField(default=False)),
                ('co_rev', models.BooleanField(default=False)),
                ('game', models.OneToOneField(to='tournament.Game', on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='PlayoffResult',
            fields=[
                ('gameresult_ptr', models.OneToOneField(
                    primary_key=True,
                    auto_created=True,
                    to='tournament.GameResult',
                    parent_link=True,
                    serialize=False, on_delete=models.CASCADE
                )),
                ('og', models.BooleanField()),
                ('oo', models.BooleanField()),
                ('cg', models.BooleanField()),
                ('co', models.BooleanField()),
            ],
            bases=('tournament.gameresult',),
        ),
        migrations.CreateModel(
            name='QualificationResult',
            fields=[
                ('gameresult_ptr', models.OneToOneField(
                    primary_key=True,
                    auto_created=True,
                    to='tournament.GameResult',
                    parent_link=True,
                    serialize=False, on_delete=models.CASCADE
                )),
                ('og', models.IntegerField()),
                ('oo', models.IntegerField()),
                ('cg', models.IntegerField()),
                ('co', models.IntegerField()),
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
            ],
            bases=('tournament.gameresult',),
        ),
    ]
