# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0002_initial_motion'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('info', models.TextField(blank=True)),
                ('speaker_1', models.ForeignKey(
                    related_name='first_speaker',
                    to=settings.AUTH_USER_MODEL,
                    on_delete=models.CASCADE
                )),
                ('speaker_2', models.ForeignKey(
                    related_name='second_speaker',
                    to=settings.AUTH_USER_MODEL,
                    on_delete=models.CASCADE
                )),
            ],
        ),
    ]
