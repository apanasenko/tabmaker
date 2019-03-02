from django.db import models
from . profile import User


class Team(models.Model):
    name = models.CharField(max_length=100)
    speaker_1 = models.ForeignKey(User, related_name='first_speaker', on_delete=models.SET_NULL, null=True)
    speaker_2 = models.ForeignKey(User, related_name='second_speaker', on_delete=models.SET_NULL, null=True)
    info = models.TextField(blank=True)

    def __str__(self):
        return "%s  %s" % (self.id, self.name)
