from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0025_separate_bot_users_and_chats'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='botusers',
            name='user_id',
        ),
        migrations.RemoveField(
            model_name='botusers',
            name='chat_id',
        ),
        migrations.RemoveField(
            model_name='botusers',
            name='chat_name',
        ),
    ]
