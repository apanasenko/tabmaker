from allauth.account.models import EmailAddress
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
    is_show_phone = models.BooleanField(default=True)
    is_show_email = models.BooleanField(default=True)

    def name(self):
        return "%s %s" % (self.first_name, self.last_name) \
            if self.last_name \
            else self.email

    def confirmation(self):
        EmailAddress.objects.create(
            user=self,
            email=self.email,
            verified=True,
            primary=True,
        )
    @staticmethod
    def get_or_create(email: str, full_name: str):
        user = User.objects.filter(email=email).last()
        if user:
            return user, True
        else:
            name = full_name.strip().split(maxsplit=1)
            name += ['', '']
            user = User.objects.create(
                email=email,
                username=email,
                last_name=name[0],
                first_name=name[1],
                phone='',
                university_id=1,
                link='https://vk.com/tabmaker',
                player_experience='',
                adjudicator_experience='',
                is_show_phone=False,
                is_show_email=False,
            )
            user.confirmation()

            return user, False
