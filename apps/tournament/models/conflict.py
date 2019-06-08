from django.db import models

from apps.tournament.models import Tournament, User, Team


class AdjudicatorConflict(models.Model):
    tournament = models.ForeignKey(
        Tournament, on_delete=models.CASCADE, related_name='conflicts'
    )
    adjudicator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='conflicts'
    )
    team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name='conflicts'
    )
