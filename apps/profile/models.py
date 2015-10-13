__author__ = 'Alexander'

from django.contrib.auth.models import AbstractUser
from django.db import models


class Country(models.Model):
    country_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)


class City(models.Model):
    city_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)


class University(models.Model):
    country = models.ForeignKey(to=Country)
    city = models.ForeignKey(to=City)
    university_id = models.IntegerField()
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('country', 'city', 'university_id')


class User(AbstractUser):
    university = models.ForeignKey(to=University, null=True)
    phone = models.CharField(max_length=15)
    link = models.CharField(max_length=100)
    player_experience = models.TextField()
    adjudicator_experience = models.TextField()

    def name(self):
        return "%s %s" % (self.first_name, self.last_name) \
            if self.last_name \
            else self.email
