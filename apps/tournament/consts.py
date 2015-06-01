__author__ = 'Alexander'

from enum import Enum
from .models import \
    TournamentRole, \
    TournamentStatus

TEAM_IN_GAME = 4

Position = Enum('Position', 'OG OO CG CO NONE')

ROLE_OWNER = TournamentRole.objects.get(role='owner')
ROLE_ADMIN = TournamentRole.objects.get(role='admin')
ROLE_CHIEF_ADJUDICATOR = TournamentRole.objects.get(role='chief_adjudicator')

ROLE_TEAM_REGISTERED = TournamentRole.objects.get(role='registered')
ROLE_IN_TAB = TournamentRole.objects.get(role='in_tab')
ROLE_WAIT_LIST = TournamentRole.objects.get(role='wait_list')
ROLE_VERIFIED = TournamentRole.objects.get(role='verified')  # Участник подтвердил участие
ROLE_APPROVED = TournamentRole.objects.get(role='approved')  # Организатор подтвердил
ROLE_MEMBER = TournamentRole.objects.get(role='member')

ROLE_ADJUDICATOR_REGISTERED = TournamentRole.objects.get(role='registered_adjudicator'),
ROLE_ADJUDICATOR_APPROVED = TournamentRole.objects.get(role='approved_adjudicator'),
ROLE_WING = TournamentRole.objects.get(role='wing')
ROLE_CHAIR = TournamentRole.objects.get(role='chair')

STATUS_REGISTRATION = TournamentStatus.objects.get(name='registration')
STATUS_PREPARATION = TournamentStatus.objects.get(name='preparation')
STATUS_STARTED = TournamentStatus.objects.get(name='started')
STATUS_FINISHED = TournamentStatus.objects.get(name='finished')
STATUS_PLAYOFF = TournamentStatus.objects.get(name='playoff')

TEAM_ROLES_NAMES = [
    'registered',
    'in_tab',
    'wait_list',
    'verified',
    'approved',
    'member',
]

ADJUDICATOR_ROLES_NAMES = [
    'registered_adjudicator',
    'approved_adjudicator',
    'wing',
    'chair',
]

TEAM_ROLES = TournamentRole.objects.filter(role__in=TEAM_ROLES_NAMES)
ADJUDICATOR_ROLES = TournamentRole.objects.filter(role__in=ADJUDICATOR_ROLES_NAMES)
