from django.db import models
from . import Language


class BotUsers(models.Model):
    user_id = models.BigIntegerField()
    username = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    chat_id = models.BigIntegerField(blank=True)
    chat_name = models.CharField(max_length=100, blank=True)
    language = models.ForeignKey(Language, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return '%d: %s %s (%s) / %s' % (self.user_id, self.first_name, self.last_name, self.username, self.chat_name)
