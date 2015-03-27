__author__ = 'Alexander'

from .models import TournamentRole


ROLE_OWNER = TournamentRole.objects.get(role='owner')
ROLE_MEMBER = TournamentRole.objects.get(role='member')
ROLE_CHAIR = TournamentRole.objects.get(role='chair')
ROLE_WING = TournamentRole.objects.get(role='wing')
ROLE_TEAM_REGISTERED = TournamentRole.objects.get(role='registered')
ROLE_ADJUDICATOR_REGISTERED = TournamentRole.objects.get(role='registered_adjudicator'),
