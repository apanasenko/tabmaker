from django.contrib import admin
from .models import \
    Place, \
    Room, \
    Round, \
    Tournament, \
    TournamentRole, \
    UserTournamentRel


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
