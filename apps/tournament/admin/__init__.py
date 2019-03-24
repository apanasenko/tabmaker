from . motion import MotionAdmin
from apps.tournament.models import Motion
from django.contrib.admin import site

site.register(Motion, MotionAdmin)
