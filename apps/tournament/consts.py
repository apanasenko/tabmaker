__author__ = 'Alexander'

from enum import Enum
from .models import \
    TournamentRole, \
    TournamentStatus

TEAM_IN_GAME = 4

Position = Enum('Position', 'OG OO CG CO NONE')

ROLE_OWNER = TournamentRole.objects.get(role_en='Owner')
ROLE_ADMIN = TournamentRole.objects.get(role_en='Admin')
ROLE_CHIEF_ADJUDICATOR = TournamentRole.objects.get(role_en='Chief adjudicator')

ROLE_TEAM_REGISTERED = TournamentRole.objects.get(role_en='Registered')
ROLE_IN_TAB = TournamentRole.objects.get(role_en='In tab')
ROLE_WAIT_LIST = TournamentRole.objects.get(role_en='Wait list')
ROLE_VERIFIED = TournamentRole.objects.get(role_en='Verified')  # Участник подтвердил участие
ROLE_APPROVED = TournamentRole.objects.get(role_en='Approved')  # Организатор подтвердил
ROLE_MEMBER = TournamentRole.objects.get(role_en='Member')

ROLE_ADJUDICATOR_REGISTERED = TournamentRole.objects.get(role_en='Registered adjudicator'),
ROLE_ADJUDICATOR_APPROVED = TournamentRole.objects.get(role_en='Approved adjudicator'),
ROLE_WING = TournamentRole.objects.get(role_en='Wing')
ROLE_CHAIR = TournamentRole.objects.get(role_en='Chair')

STATUS_REGISTRATION = TournamentStatus.objects.get(name='registration')
STATUS_PREPARATION = TournamentStatus.objects.get(name='preparation')
STATUS_STARTED = TournamentStatus.objects.get(name='started')
STATUS_FINISHED = TournamentStatus.objects.get(name='finished')
STATUS_PLAYOFF = TournamentStatus.objects.get(name='playoff')

TEAM_ROLES_NAMES = [
    'Registered',
    'In tab',
    'Wait list',
    'Verified',
    'Approved',
    'Member',
]

ADJUDICATOR_ROLES_NAMES = [
    'Registered adjudicator',
    'Approved adjudicator',
    'Wing',
    'Chair',
]

TEAM_ROLES = TournamentRole.objects.filter(role_en__in=TEAM_ROLES_NAMES)
ADJUDICATOR_ROLES = TournamentRole.objects.filter(role_en__in=ADJUDICATOR_ROLES_NAMES)
