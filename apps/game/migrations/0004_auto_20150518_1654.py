# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_auto_20150515_1619'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gameresult',
            old_name='Deputy Leader of Opposition',
            new_name='dlo',
        ),
        migrations.RenameField(
            model_name='gameresult',
            old_name='Deputy Prime Minister',
            new_name='dpm',
        ),
        migrations.RenameField(
            model_name='gameresult',
            old_name='Government Whip',
            new_name='gw',
        ),
        migrations.RenameField(
            model_name='gameresult',
            old_name='Leader of Opposition',
            new_name='lo',
        ),
        migrations.RenameField(
            model_name='gameresult',
            old_name='Member of Government',
            new_name='mg',
        ),
        migrations.RenameField(
            model_name='gameresult',
            old_name='Member of Opposition',
            new_name='mo',
        ),
        migrations.RenameField(
            model_name='gameresult',
            old_name='Opposition Whip',
            new_name='ow',
        ),
        migrations.RenameField(
            model_name='gameresult',
            old_name='Prime Minister',
            new_name='pm',
        ),
    ]
