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
    url(r'^(?P<tournament_id>\d+)/play[/]$', views.play, name='play'),
    url(r'^(?P<tournament_id>\d+)/team/list[/]$', views.show_team_list, name='team_list'),
    url(r'^(?P<tournament_id>\d+)/team/edit[/]$', views.edit_team_list, name='edit_team_list'),
    url(r'^(?P<tournament_id>\d+)/team/check[/]$', views.edit_team_list, name='check_team_list'),
    url(r'^(?P<tournament_id>\d+)/team/registration[/]$', views.registration_team, name='registration_team'),
    url(r'^(?P<tournament_id>\d+)/adjudicator/list[/]$', views.show_adjudicator_list, name='adjudicator_list'),
    url(r'^(?P<tournament_id>\d+)/adjudicator/edit[/]$', views.edit_adjudicator_list, name='edit_adjudicator_list'),
    url(r'^(?P<tournament_id>\d+)/adjudicator/check[/]$', views.edit_adjudicator_list, name='check_adjudicator_list'),
    url(
        r'^(?P<tournament_id>\d+)/adjudicator/registration[/]$',
        views.registration_adjudicator,
        name='registration_adjudicator'
    ),

)
