from django.db import models

from apps.tournament.models import QualificationResult

PLACE_TO_SCORE = 8


class MotionAnalysis(models.Model):
    motion = models.OneToOneField(
        to='tournament.Motion',
        on_delete=models.CASCADE,
        related_name='analysis'
    )
    government_score = models.IntegerField()
    opposition_score = models.IntegerField()

    def generate_analysis(self, motion):
        games = motion.game_set.all()
        self.government_score = 0
        self.opposition_score = 0
        for _ in games:
            for result in QualificationResult.objects.filter(game=_):
                self.government_score += PLACE_TO_SCORE - result.og - result.cg
                self.opposition_score += PLACE_TO_SCORE - result.oo - result.co

        self.motion = motion
        self.save()
