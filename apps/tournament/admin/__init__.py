from . motion import MotionAdmin
from . tournament import TournamentAdmin
from apps.tournament.models import Motion, Language, BotUsers, BotChat, Tournament
from django.contrib.admin import site

site.register(Motion, MotionAdmin)
site.register(Language)
site.register(BotUsers)
site.register(BotChat)
site.register(Tournament, TournamentAdmin)
