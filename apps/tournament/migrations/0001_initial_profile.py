# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import migrations, models
import django.utils.timezone
import django.core.validators
import django.contrib.auth.models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('city_id', models.IntegerField(unique=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('country_id', models.IntegerField(unique=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='University',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('university_id', models.IntegerField()),
                ('name', models.CharField(max_length=100)),
                ('city', models.ForeignKey(to='tournament.City')),
                ('country', models.ForeignKey(to='tournament.Country')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='university',
            unique_together={('country', 'city', 'university_id')},
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', blank=True, null=True)),
                ('is_superuser', models.BooleanField(
                    verbose_name='superuser status',
                    help_text='Designates that this user has all permissions without explicitly assigning them.',
                    default=False
                )),
                ('username', models.CharField(
                    verbose_name='username',
                    help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.',
                    error_messages={'unique': 'A user with that username already exists.'},
                    validators=[django.core.validators.RegexValidator(
                        '^[\\w.@+-]+$',
                        'Enter a valid username. '
                        + 'This value may contain only letters, numbers and @/./+/-/_ characters.',
                        'invalid'
                    )],
                    unique=True,
                    max_length=30
                )),
                ('first_name', models.CharField(verbose_name='first name', blank=True, max_length=30)),
                ('last_name', models.CharField(verbose_name='last name', blank=True, max_length=30)),
                ('email', models.EmailField(verbose_name='email address', blank=True, max_length=254)),
                ('is_staff', models.BooleanField(
                    verbose_name='staff status',
                    help_text='Designates whether the user can log into this admin site.',
                    default=False
                )),
                ('is_active', models.BooleanField(
                    verbose_name='active',
                    help_text='Designates whether this user should be treated as active. '
                              + 'Unselect this instead of deleting accounts.',
                    default=True
                )),
                ('date_joined', models.DateTimeField(verbose_name='date joined', default=django.utils.timezone.now)),
                ('phone', models.CharField(max_length=15)),
                ('link', models.CharField(max_length=100)),
                ('player_experience', models.TextField()),
                ('adjudicator_experience', models.TextField()),
                ('is_show_phone', models.BooleanField(default=True)),
                ('is_show_email', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(
                    verbose_name='groups',
                    help_text='The groups this user belongs to. '
                              + 'A user will get all permissions granted to each of their groups.',
                    related_name='user_set', to='auth.Group', related_query_name='user',
                    blank=True
                )),
                ('university', models.ForeignKey(null=True, to='tournament.University')),
                ('user_permissions', models.ManyToManyField(
                    verbose_name='user permissions',
                    help_text='Specific permissions for this user.',
                    related_name='user_set', to='auth.Permission',
                    related_query_name='user', blank=True
                )),
            ],
            options={
                'verbose_name': 'user',
                'abstract': False,
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
