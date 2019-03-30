from . motion import MotionAdmin
from apps.tournament.models import Motion, Language, BotUsers
from django.contrib.admin import site

site.register(Motion, MotionAdmin)
site.register(Language)
site.register(BotUsers)
