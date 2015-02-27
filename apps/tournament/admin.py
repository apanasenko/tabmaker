from django.contrib import admin
from apps.tournament.models import Place
from apps.tournament.models import Room
from apps.tournament.models import Round
from apps.tournament.models import Tournament
from apps.tournament.models import TournamentRole
from apps.tournament.models import UserTournamentRel


models = [
    Place,
    Room,
    Round,
    Tournament,
    TournamentRole,
    UserTournamentRel,
]

for model in models:
    admin.site.register(model)
