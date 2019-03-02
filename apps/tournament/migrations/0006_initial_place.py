# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0005_initial_tournament'),
    ]

    operations = [
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('place', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=True)),
                ('tournament', models.ForeignKey(to='tournament.Tournament', on_delete=models.CASCADE)),
            ],
        ),
    ]
