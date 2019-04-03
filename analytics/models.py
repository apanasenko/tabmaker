from django.db import models

from apps.tournament.models import QualificationResult


class MotionAnalysis(models.Model):
    motion = models.OneToOneField(
        to='tournament.Motion',
        on_delete=models.CASCADE,
        related_name='analysis'
    )
    government_score = models.IntegerField(default=0)
    opposition_score = models.IntegerField(default=0)

    def generate_analysis(self, motion):
        games = motion.game_set.all()
        for _ in games:
            for result in QualificationResult.objects.filter(game=_):
                self.government_score += 8 - result.og - result.cg
                self.opposition_score += 8 - result.oo - result.co

        self.motion = motion
        self.save()
