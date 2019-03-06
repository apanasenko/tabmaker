from django.db import models


class MotionAnalysis(models.Model):
    motion = models.OneToOneField(to='tournament.Motion', on_delete=models.CASCADE, related_name='analysis')
    government_score = models.IntegerField(default=0)
    opposition_score = models.IntegerField(default=0)
