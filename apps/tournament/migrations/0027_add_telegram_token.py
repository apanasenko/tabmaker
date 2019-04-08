from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0026_botusers_remove_old_fields'),
    ]

    operations = [
        migrations.CreateModel(
            name='TelegramToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.TextField(max_length=64)),
                ('expire', models.DateTimeField()),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='telegram',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tournament.BotUsers'),
        ),
        migrations.AddField(
            model_name='telegramtoken',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
