from django.db import models
from . profile import User


class Team(models.Model):
    name = models.CharField(max_length=100)
    speaker_1 = models.ForeignKey(User, related_name='first_speaker', on_delete=models.SET_NULL, null=True)
    speaker_2 = models.ForeignKey(User, related_name='second_speaker', on_delete=models.SET_NULL, null=True)
    info = models.TextField(blank=True)

    def get_speakers(self) -> [User]:
        return [self.speaker_1, self.speaker_2]

    def __str__(self):
        return "%s  %s" % (self.id, self.name)
