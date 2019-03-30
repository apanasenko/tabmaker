from . motion import MotionAdmin
from apps.tournament.models import Motion, Language
from django.contrib.admin import site

site.register(Motion, MotionAdmin)
site.register(Language)
