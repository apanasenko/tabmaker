from django.db import models
from . profile import User
from . team import Team


class TournamentStatus(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class TournamentRole(models.Model):
    name = models.CharField(max_length=100, name='role')

    def __str__(self):
        return self.role


class Tournament(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=500)
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
    is_registration_hidden = models.BooleanField(default=False)

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
        from ..consts import ROLE_MEMBER
        return self.teamtournamentrel_set.filter(role=ROLE_MEMBER).count()

    def count_registered_teams(self):
        return self.teamtournamentrel_set.count()

    def __str__(self):
        return self.name


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
