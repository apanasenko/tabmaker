from django.db import models
from django.contrib.auth.models import User


class Team(models.Model):
    name = models.CharField(max_length=100)
    speaker_1 = models.ForeignKey(User, related_name='first_speaker')
    speaker_2 = models.ForeignKey(User, related_name='second_speaker')
    info = models.TextField()
