from django.db import models

# User >>>
from allauth.account.models import EmailAddress
from django.contrib.auth.models import AbstractUser
from django.core.mail import EmailMultiAlternatives
# from django.db import models
from django.template.loader import get_template
from django.template import Context
from DebatesTournament.settings.smtp_email import EMAIL_HOST_USER


class Country(models.Model):
    class Meta:
        app_label = 'profile'

    country_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)


class City(models.Model):
    class Meta:
        app_label = 'profile'

    city_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)


class University(models.Model):
    class Meta:
        app_label = 'profile'
        unique_together = ('country', 'city', 'university_id')

    country = models.ForeignKey(to=Country)
    city = models.ForeignKey(to=City)
    university_id = models.IntegerField()
    name = models.CharField(max_length=100)


class User(AbstractUser):
    class Meta:
        app_label = 'profile'

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

# <<<<


class Motion(models.Model):
    motion = models.TextField()
    infoslide = models.TextField(blank=True)


class Team(models.Model):
    name = models.CharField(max_length=100)
    speaker_1 = models.ForeignKey(User, related_name='first_speaker')
    speaker_2 = models.ForeignKey(User, related_name='second_speaker')
    info = models.TextField(blank=True)

    def __str__(self):
        return "%s  %s" % (self.id, self.name)


# OG = Opening Government (Prime Minister & Deputy Prime Minister)
# OO = Opening Opposition (Leader of Opposition & Deputy Leader of Opposition)
# CG = Closing Government (Member of Government & Government Whip)
# CO = Closing Opposition (Member of Opposition & Opposition Whip)


class Game(models.Model):
    og = models.ForeignKey(Team, related_name='OG')
    oo = models.ForeignKey(Team, related_name='OO')
    cg = models.ForeignKey(Team, related_name='CG')
    co = models.ForeignKey(Team, related_name='CO')
    chair = models.ForeignKey(User, related_name='chair')
    wing_left = models.ForeignKey(User, related_name='wing_left', blank=True, null=True)
    wing_right = models.ForeignKey(User, related_name='wing_right', blank=True, null=True)
    motion = models.ForeignKey(Motion)
    date = models.DateTimeField()


class GameResult(models.Model):
    game = models.OneToOneField(Game)

    # Place
    og = models.IntegerField()
    oo = models.IntegerField()
    cg = models.IntegerField()
    co = models.IntegerField()

    # Position of speakers (true - if speakers were in the reverse order)
    og_rev = models.BooleanField(default=False)
    oo_rev = models.BooleanField(default=False)
    cg_rev = models.BooleanField(default=False)
    co_rev = models.BooleanField(default=False)

    # Speaker's points
    # OG (Prime Minister & Deputy Prime Minister)
    pm = models.IntegerField()
    pm_exist = models.BooleanField(default=True)
    dpm = models.IntegerField()
    dpm_exist = models.BooleanField(default=True)

    # OO (Leader of Opposition & Deputy Leader of Opposition)
    lo = models.IntegerField()
    lo_exist = models.BooleanField(default=True)
    dlo = models.IntegerField()
    dlo_exist = models.BooleanField(default=True)

    # CG (Member of Government & Government Whip)
    mg = models.IntegerField()
    mg_exist = models.BooleanField(default=True)
    gw = models.IntegerField()
    gw_exist = models.BooleanField(default=True)

    # CO (Member of Opposition & Opposition Whip)
    mo = models.IntegerField()
    mo_exist = models.BooleanField(default=True)
    ow = models.IntegerField()
    ow_exist = models.BooleanField(default=True)

    @staticmethod
    def to_dict(team, place, s1, s2, rev):
        return {'team': team, 'place': place, 'speaker_1': s1, 'speaker_2': s2, 'revert': rev}

    def get_og_result(self):
        return self.to_dict(self.game.og, self.og, self.pm, self.dpm, self.og_rev)

    def get_oo_result(self):
        return self.to_dict(self.game.oo, self.oo, self.lo, self.dlo, self.oo_rev)

    def get_cg_result(self):
        return self.to_dict(self.game.cg, self.cg, self.mg, self.gw, self.cg_rev)

    def get_co_result(self):
        return self.to_dict(self.game.co, self.co, self.mo, self.ow, self.co_rev)


class TournamentStatus(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tournament(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    location_lon = models.FloatField(default=43.024658672481465)
    location_lat = models.FloatField(default=131.89274039289919)
    open_reg = models.DateTimeField('open registration')
    close_reg = models.DateTimeField('close registration')
    start_tour = models.DateTimeField('start tournament')
    count_rounds = models.PositiveIntegerField()
    count_teams = models.PositiveIntegerField()
    count_teams_in_break = models.PositiveIntegerField()
    link = models.URLField(blank=True, null=True)
    user_members = models.ManyToManyField(User, through='UserTournamentRel')
    team_members = models.ManyToManyField(Team, through='TeamTournamentRel')
    status = models.ForeignKey(TournamentStatus, null=True)
    cur_round = models.PositiveIntegerField(default=0)
    info = models.TextField()

    def round_number_inc(self):
        self.cur_round += 1
        self.save()
        return self.cur_round

    def round_number_dec(self):
        self.cur_round -= 1
        self.save()
        return self.cur_round

    def set_status(self, status: TournamentStatus):
        self.status = status
        self.save()

    def get_users(self, roles=None):
        return self.usertournamentrel_set \
            .filter(role__in=roles) \
            .order_by('user_id') \
            .select_related('user') \
            .select_related('role')

    def get_teams(self, roles=None):
            q = self.teamtournamentrel_set
            q = q.filter(role__in=roles) if roles else q.all()
            for i in ['team', 'role', 'team__speaker_1', 'team__speaker_2']:
                q = q.select_related(i)
            return q.order_by('-role_id', '-id')

    def count_members(self):
        from .consts import ROLE_MEMBER
        return self.teamtournamentrel_set.filter(role=ROLE_MEMBER).count()

    def count_registered_teams(self):
        return self.teamtournamentrel_set.count()

    def __str__(self):
        return self.name


class Place(models.Model):
    tournament = models.ForeignKey(Tournament)
    place = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

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

    def __str__(self):
        return '%s: %s - %s' % (self.id, self.user.name(), self.role.role)


class TeamTournamentRel(models.Model):
    team = models.ForeignKey(Team)
    tournament = models.ForeignKey(Tournament)
    role = models.ForeignKey(TournamentRole)

    def __str__(self):
        return '%s: %s - %s' % (self.id, self.team.name, self.role.role)


class Round(models.Model):
    tournament = models.ForeignKey(Tournament)
    motion = models.ForeignKey(Motion)
    number = models.IntegerField()
    start_time = models.DateTimeField()
    is_closed = models.BooleanField(default=False)
    is_public = models.BooleanField(default=True)
    is_playoff = models.BooleanField(default=False)

    def publish(self):
        self.is_public = True
        self.save()


class Room(models.Model):
    round = models.ForeignKey(Round)
    game = models.ForeignKey(Game)
    place = models.ForeignKey(Place, blank=True, null=True, on_delete=models.SET_NULL)
    number = models.IntegerField(blank=True)


class Page(models.Model):
    name = models.CharField(max_length=100)
    is_public = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class AccessToPage(models.Model):
    page = models.ForeignKey(Page)
    status = models.ForeignKey(TournamentStatus)
    access = models.BooleanField(default=True)
    message = models.TextField(blank=True, null=True)


# ###################### #
#      Custom Forms      #
# ###################### #

class CustomFormType(models.Model):
    name = models.CharField(max_length=100)


class CustomFieldAlias(models.Model):
    name = models.CharField(max_length=100)


class CustomForm(models.Model):
    tournament = models.ForeignKey(Tournament)
    form_type = models.ForeignKey(CustomFormType)

    @staticmethod
    def get_or_create(tournament: Tournament, form_type: CustomFormType):
        from .consts import CUSTOM_FIELD_SETS

        form = CustomForm.objects.get_or_create(tournament=tournament, form_type=form_type)
        if form[1] and form_type in CUSTOM_FIELD_SETS:  # is create
            fields = CUSTOM_FIELD_SETS[form_type]
            for i in range(len(fields)):
                CustomQuestion.objects.create(
                    question=fields[i][1],
                    comment='',
                    position=(i + 1),
                    required=fields[i][2],
                    form=form[0],
                    alias=fields[i][0]
                )

        return form[0]


class CustomQuestion(models.Model):
    question = models.CharField(max_length=300)
    comment = models.TextField()
    position = models.PositiveIntegerField()
    required = models.BooleanField(default=True)
    form = models.ForeignKey(CustomForm)
    alias = models.ForeignKey(CustomFieldAlias, blank=True, null=True)


class CustomFormAnswers(models.Model):
    form = models.ForeignKey(CustomForm)
    answers = models.TextField()

    @staticmethod
    def save_answer(custom_form, answers):
        import json
        return CustomFormAnswers.objects.create(form=custom_form, answers=json.dumps(answers))

    @staticmethod
    def get_answers(custom_form):
        import json
        return list(map(
            lambda x: json.loads(x.answers),
            CustomFormAnswers.objects.filter(form=custom_form).order_by('id')
        ))
