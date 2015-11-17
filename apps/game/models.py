from django.db import models
from apps.motion.models import Motion
from apps.team.models import Team
from apps.profile.models import User


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
