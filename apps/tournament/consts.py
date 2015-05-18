__author__ = 'Alexander'

from .models import \
    TournamentRole, \
    TournamentStatus

TEAM_IN_GAME = 4

ROLE_OWNER = TournamentRole.objects.get(role='owner')
ROLE_MEMBER = TournamentRole.objects.get(role='member')
ROLE_CHAIR = TournamentRole.objects.get(role='chair')
ROLE_WING = TournamentRole.objects.get(role='wing')
ROLE_TEAM_REGISTERED = TournamentRole.objects.get(role='registered')
ROLE_ADJUDICATOR_REGISTERED = TournamentRole.objects.get(role='registered_adjudicator'),

STATUS_REGISTRATION = TournamentStatus.objects.get(name='registration')
STATUS_PREPARATION = TournamentStatus.objects.get(name='preparation')
STATUS_STARTED = TournamentStatus.objects.get(name='started')
STATUS_FINISHED = TournamentStatus.objects.get(name='finished')
