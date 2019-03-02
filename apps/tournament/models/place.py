from django.db import models
from . tournament import Tournament


class Place(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    place = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.place

