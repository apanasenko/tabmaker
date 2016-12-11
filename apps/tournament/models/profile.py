from allauth.account.models import EmailAddress
from DebatesTournament.settings.smtp_email import EMAIL_HOST_USER
from django.contrib.auth.models import AbstractUser
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.template import Context
from django.template.loader import get_template


class Country(models.Model):
    country_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)


class City(models.Model):
    city_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)


class University(models.Model):
    class Meta:
        unique_together = ('country', 'city', 'university_id')

    country = models.ForeignKey(to=Country)
    city = models.ForeignKey(to=City)
    university_id = models.IntegerField()
    name = models.CharField(max_length=100)


class User(AbstractUser):
    university = models.ForeignKey(to=University, null=True)
    phone = models.CharField(max_length=15)
    link = models.URLField(max_length=100, default='', blank=True)
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
        user = User.objects.filter(email=email).last()
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
