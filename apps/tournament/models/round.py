from django.db import models
from . motion import Motion
from . tournament import Tournament


class Round(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    motion = models.ForeignKey(Motion, on_delete=models.CASCADE)
    number = models.IntegerField()
    start_time = models.DateTimeField()
    is_closed = models.BooleanField(default=False)
    is_public = models.BooleanField(default=True)
    is_playoff = models.BooleanField(default=False)

    def publish(self):
        self.is_public = True
        self.save()

