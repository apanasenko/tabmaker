from apps.profile.models import User
from django.db import models
from apps.game.models import Game
from apps.motion.models import Motion
from apps.team.models import Team

import pytz


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

    def save(self, *args, **kwargs):
        self.open_reg = self.open_reg.astimezone(pytz.utc)
        self.close_reg = self.close_reg.astimezone(pytz.utc)
        self.start_tour = self.start_tour.astimezone(pytz.utc)
        super(Tournament, self).save(*args, **kwargs)

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
    tournament = models.OneToOneField(Tournament)
    link = models.TextField(default='')
    form_type = models.ForeignKey(CustomFormType)

    @staticmethod
    def get_or_create(tournament: Tournament, form_type: CustomFormType):
        from .consts import CUSTOM_FIELD_SETS

        form = CustomForm.objects.get_or_create(tournament=tournament, form_type=form_type)
        if form[1]:  # is create
            for i in range(len(CUSTOM_FIELD_SETS)):
                CustomQuestion.objects.create(
                    question=CUSTOM_FIELD_SETS[i][1],
                    comment='',
                    position=(i + 1),
                    required=CUSTOM_FIELD_SETS[i][2],
                    form=form[0],
                    alias=CUSTOM_FIELD_SETS[i][0]
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
