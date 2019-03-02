from django.db import models
from . tournament import TournamentStatus


class Page(models.Model):
    name = models.CharField(max_length=100)
    is_public = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class AccessToPage(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    status = models.ForeignKey(TournamentStatus, on_delete=models.CASCADE)
    access = models.BooleanField(default=True)
    message = models.TextField(blank=True, null=True)

