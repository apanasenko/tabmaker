__author__ = 'Alexander'

from . import views
from django.conf.urls import \
    patterns, \
    url


urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^new[/]$', views.new, name='new'),
    url(r'^(?P<tournament_id>\d+)[/]$', views.show, name='show'),
    url(r'^(?P<tournament_id>\d+)/edit[/]$', views.edit, name='edit'),
    url(r'^(?P<tournament_id>\d+)/registration/team[/]$', views.registration_team, name='registration_team'),
    url(
        r'^(?P<tournament_id>\d+)/registration/adjudicator[/]$',
        views.registration_adjudicator,
        name='registration_adjudicator'
    ),
    url(r'^(?P<tournament_id>\d+)/teams/list[/]$', views.show_team_list, name='team_list'),
    url(r'^(?P<tournament_id>\d+)/teams/edit[/]$', views.edit_team_list, name='edit_team_list'),
    url(r'^(?P<tournament_id>\d+)/adjudicator/list[/]$', views.show_adjudicator_list, name='adjudicator_list'),
)
