__author__ = 'Alexander'

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    country_vk_id = models.IntegerField(default=0)
    city_vk_id = models.IntegerField(default=0)
    university_vk_id = models.IntegerField(default=0)
    phone = models.CharField(max_length=15)
    link = models.CharField(max_length=100)
    player_experience = models.TextField()
    adjudicator_experience = models.TextField()
