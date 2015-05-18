from django.db import models


class Motion(models.Model):
    motion = models.TextField()
    infoslide = models.TextField(blank=True)
