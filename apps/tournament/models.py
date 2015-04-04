from apps.profile.models import User
from django.db import models
from apps.game.models import Game
from apps.motion.models import Motion
from apps.team.models import Team

import pytz


class Tournament(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)  # TODO Посмотреть форма данный связанный с геолокацией
    open_reg = models.DateTimeField('open registration')
    close_reg = models.DateTimeField('close registration')
    start_tour = models.DateTimeField('start tournament')
    count_rounds = models.IntegerField()
    is_closed = models.BooleanField(default=False)
    user_members = models.ManyToManyField(User, through='UserTournamentRel')
    team_members = models.ManyToManyField(Team, through='TeamTournamentRel')
    info = models.TextField()

    def save(self, *args, **kwargs):
        self.open_reg = self.open_reg.astimezone(pytz.utc)
        self.close_reg = self.close_reg.astimezone(pytz.utc)
        self.start_tour = self.start_tour.astimezone(pytz.utc)
        super(Tournament, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Place(models.Model):
    tournament = models.ForeignKey(Tournament)
    place = models.CharField(max_length=100)

    def __str__(self):
        return self.place


class TournamentRole(models.Model):
    name = models.CharField(max_length=100, name='role')

    def __str__(self):
        return self.role


class UserTournamentRel(models.Model):
    user = models.ForeignKey(User)
    tournament = models.ForeignKey(Tournament)
    role = models.ForeignKey(TournamentRole)


class TeamTournamentRel(models.Model):
    team = models.ForeignKey(Team)
    tournament = models.ForeignKey(Tournament)
    role = models.ForeignKey(TournamentRole)


class Round(models.Model):
    tournament = models.ForeignKey(Tournament)
    motion = models.ForeignKey(Motion)
    number = models.IntegerField()
    start_time = models.DateTimeField()
    is_closed = models.BooleanField(default=False)


class Room(models.Model):
    round = models.ForeignKey(Round)
    game = models.ForeignKey(Game)
    place = models.ForeignKey(Place, blank=True, null=True, on_delete=models.SET_NULL)
