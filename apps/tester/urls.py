__author__ = 'Alexander'

from . import views
from django.conf.urls import \
    patterns, \
    url


urlpatterns = patterns('',
   url(
       r'^generate/(?P<tournament_id>\d+)/(?P<func>(team|adjudicator))/(?P<role_id>\d+)/(?P<count>\d+)[/]$',
       views.generate
   )
)
