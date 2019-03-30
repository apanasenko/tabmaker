# Generated by Django 2.1.7 on 2019-03-30 16:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0021_add_on_delete_rules'),
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('telegram_bot_label', models.TextField(blank=True)),
                ('is_public', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='motion',
            name='language',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to='tournament.Language'
            ),
        ),
    ]
