from django.db import models
from . language import Language


class BotUsers(models.Model):
    id = models.BigIntegerField(primary_key=True)
    username = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    language = models.ForeignKey(Language, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return '%d (%s): %s %s' % (self.id, self.username, self.first_name, self.last_name)


class BotChat(models.Model):
    id = models.BigIntegerField(primary_key=True)
    title = models.CharField(max_length=100, blank=True)
    language = models.ForeignKey(Language, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return '%d: %s' % (self.id, self.title)
