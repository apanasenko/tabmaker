from django.db import models


class Language(models.Model):
    name = models.TextField(blank=False)
    telegram_bot_label = models.TextField(blank=True)
    is_public = models.BooleanField(default=False)


class Motion(models.Model):
    motion = models.TextField()
    infoslide = models.TextField(blank=True)
    is_public = models.BooleanField(default=False)
    language = models.ForeignKey(Language, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return '%d: (%d) %s' % (self.id, self.is_public, self.motion)
