from django.db import models


class BotUsers(models.Model):
    user_id = models.PositiveIntegerField()
    username = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    chat_id = models.IntegerField(blank=True)
    chat_name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return '%d: %s %s (%s) / %s' % (self.user_id, self.first_name, self.last_name, self.username, self.chat_name)

