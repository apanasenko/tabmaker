from django.db import models


class Language(models.Model):
    name = models.TextField(blank=False)
    telegram_bot_label = models.TextField(blank=True)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return self.name
