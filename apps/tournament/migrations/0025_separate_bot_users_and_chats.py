from django.db import migrations, models


def separate_bot_users_and_chats(apps, schema_editor):
    BotChat = apps.get_model('tournament', 'BotChat')
    BotUsers = apps.get_model('tournament', 'BotUsers')

    chats = {}
    for user in BotUsers.objects.all():
        if user.chat_id == user.user_id:
            continue

        if user.chat_id not in chats:
            chats[user.chat_id] = BotChat(id=user.chat_id, title=user.chat_name)

    for bot_chat in chats.values():
        bot_chat.save()


def unique_bot_users(apps, schema_editor):
    BotUsers = apps.get_model('tournament', 'BotUsers')

    users = {}
    for user in BotUsers.objects.all():
        if user.user_id not in users:
            user.id = user.user_id
            users[user.user_id] = user
            continue

        user.delete()

    BotUsers.objects.update(id=models.F('user_id'))


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0024_botusers_change_id_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='BotChat',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=100)),
                ('language', models.ForeignKey(blank=True, null=True, on_delete=models.deletion.SET_NULL, to='tournament.Language')),
            ],
        ),
        migrations.RunPython(separate_bot_users_and_chats),
        migrations.RunPython(unique_bot_users),
    ]
