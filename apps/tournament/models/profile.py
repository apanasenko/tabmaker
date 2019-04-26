import string, random, datetime

from allauth.account.models import EmailAddress
from DebatesTournament.settings.smtp_email import EMAIL_HOST_USER
from django.contrib.auth.models import AbstractUser
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.template import Context
from django.template.loader import get_template
from .bot_users  import BotUsers

class Country(models.Model):
    country_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)


class City(models.Model):
    city_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)


class University(models.Model):
    class Meta:
        unique_together = ('country', 'city', 'university_id')

    country = models.ForeignKey(to=Country, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(to=City, on_delete=models.SET_NULL, null=True)
    university_id = models.IntegerField()
    name = models.CharField(max_length=100)


class User(AbstractUser):
    university = models.ForeignKey(to=University, null=True, on_delete=models.SET_NULL)
    phone = models.CharField(max_length=15)
    link = models.URLField(max_length=100, default='', blank=True)
    player_experience = models.TextField(blank=True)
    adjudicator_experience = models.TextField(blank=True)
    is_show_phone = models.BooleanField(default=True)
    is_show_email = models.BooleanField(default=True)
    telegram = models.ForeignKey(BotUsers, models.SET_NULL, null=True)

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

    def send_email_about_import(self, tournament, password):
        email = EmailMultiAlternatives(
            get_template('account/email/email_import_signup_subject.txt').render().strip(),
            get_template('account/email/email_import_signup_message.txt').render(Context({
                'user': self,
                'tournament': tournament,
                'password': password,
            })),
            EMAIL_HOST_USER,
            [self.email]
        )
        email.attach_alternative(
            get_template('account/email/email_import_signup_message.html').render(Context({
                'user': self,
                'tournament': tournament,
                'password': password,
            })),
            "text/html"
        )
        email.send()

    def set_random_password(self):
        password = User.objects.make_random_password()
        self.set_password(password)
        self.save()
        return password

    @staticmethod
    def get_or_create(email: str, full_name: str, is_test=False):
        user = User.objects.filter(email__iexact=email).last()
        if user:
            return user, True
        else:
            name = full_name.strip().split(maxsplit=1)
            name += ['', '']

            # User() - создаёт объект, но не сохраняет в базу
            # User.objects.create() - сохраняет в базу
            user_obj = User if is_test else User.objects.create

            user = user_obj(
                email=email,
                username=email[:29],
                last_name=name[0][:29],
                first_name=name[1][:29],
                phone='',
                university_id=1,
                link='https://vk.com/tabmaker',
                player_experience='',
                adjudicator_experience='',
                is_show_phone=False,
                is_show_email=False,
            )
            if not is_test:
                user.confirmation()

            return user, False


class TelegramToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.TextField(max_length=64)
    expire = models.DateTimeField()

    @staticmethod
    def generate(user: User):
        token = TelegramToken(
            user=user,
            expire=datetime.datetime.now() + datetime.timedelta(days=3),
            value=(''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(30)))
        )
        token.save()
        return token
