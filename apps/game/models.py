from django.db import models
from apps.motion.models import Motion
from apps.team.models import Team
from apps.profile.models import User


# OG = Opening Government (Prime Minister & Deputy Prime Minister)
# OO = Opening Opposition (Leader of Opposition & Deputy Leader of Opposition)
# CG = Closing Government (Member of Government & Government Whip)
# CO = Closing Opposition (Member of Opposition & Opposition Whip)


class Game(models.Model):
    og = models.ForeignKey(Team, name='Opening Government', related_name='OG')
    oo = models.ForeignKey(Team, name='Opening Opposition', related_name='OO')
    cg = models.ForeignKey(Team, name='Closing Government', related_name='CG')
    co = models.ForeignKey(Team, name='Closing Opposition', related_name='CO')
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
    pm = models.IntegerField(name='Prime Minister')
    dpm = models.IntegerField(name='Deputy Prime Minister')

    # OO (Leader of Opposition & Deputy Leader of Opposition)
    lo = models.IntegerField(name='Leader of Opposition')
    dlo = models.IntegerField(name='Deputy Leader of Opposition')

    # CG (Member of Government & Government Whip)
    mg = models.IntegerField(name='Member of Government')
    gw = models.IntegerField(name='Government Whip')

    # CO (Member of Opposition & Opposition Whip)
    mo = models.IntegerField(name='Member of Opposition')
    ow = models.IntegerField(name='Opposition Whip')
