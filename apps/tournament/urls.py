__author__ = 'Alexander'

from django.conf.urls import patterns, url
from apps.tournament import views


urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^new[/]$', views.new, name='new'),
    url(r'^(?P<tournament_id>\d+)[/]$', views.show, name='show'),
    url(r'^(?P<tournament_id>\d+)/edit[/]$', views.edit, name='edit'),
    url(r'^(?P<tournament_id>\d+)/registration[/]$', views.registration, name='registration'),
    url(r'^(?P<tournament_id>\d+)/teams/list[/]$', views.show_team_list, name='team_list'),
)
