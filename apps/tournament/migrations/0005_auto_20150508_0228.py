# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0004_auto_20150410_1659'),
    ]

    operations = [
        migrations.CreateModel(
            name='TournamentStatus',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='tournament',
            name='is_closed',
        ),
        migrations.AddField(
            model_name='tournament',
            name='status',
            field=models.ForeignKey(null=True, to='tournament.TournamentStatus'),
            preserve_default=True,
        ),
    ]
