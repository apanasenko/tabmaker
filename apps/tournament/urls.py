from . import views
from django.conf.urls import \
    patterns, \
    url


urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^new[/]$', views.new, name='new'),
    url(r'^(?P<tournament_id>\d+)[/]$', views.show, name='show'),
    url(r'^(?P<tournament_id>\d+)/edit[/]$', views.edit, name='edit'),
    url(r'^(?P<tournament_id>\d+)/play[/]$', views.play, name='play'),
    url(r'^(?P<tournament_id>\d+)/break[/]$', views.generate_break, name='break'),
    url(r'^(?P<tournament_id>\d+)/result[/]$', views.result, name='result'),
    url(r'^(?P<tournament_id>\d+)/finished[/]$', views.finished, name='finished'),
    url(r'^(?P<tournament_id>\d+)/remove[/]$', views.remove, name='remove'),
    url(
        r'^(?P<tournament_id>\d+)/registration/(?P<action>(opening|closing))[/]$',
        views.registration_action,
        name='registration_action'
    ),
    url(r'^(?P<tournament_id>\d+)/round/next[/]$', views.next_round, name='next_round'),
    url(r'^(?P<tournament_id>\d+)/round/show[/]$', views.show_current_round, name='show_round'),
    url(r'^(?P<tournament_id>\d+)/round/edit[/]$', views.edit_round, name='edit_round'),
    url(r'^(?P<tournament_id>\d+)/round/result[/]$', views.result_round, name='result_round'),
    url(r'^(?P<tournament_id>\d+)/round/remove[/]$', views.remove_round, name='remove_round'),
    url(r'^(?P<tournament_id>\d+)/team/add[/]$', views.add_team, name='add_team'),
    url(r'^(?P<tournament_id>\d+)/team/list[/]$', views.edit_team_list, name='edit_team_list'),
    url(r'^(?P<tournament_id>\d+)/team/check[/]$', views.edit_team_list, name='check_team_list'),
    url(r'^(?P<tournament_id>\d+)/team/remove[/]$', views.remove_team, name='remove_team'),
    url(r'^(?P<tournament_id>\d+)/team/registration[/]$', views.registration_team, name='registration_team'),
    url(r'^(?P<tournament_id>\d+)/adjudicator/edit[/]$', views.edit_adjudicator_list, name='edit_adjudicator_list'),
    url(r'^(?P<tournament_id>\d+)/adjudicator/check[/]$', views.edit_adjudicator_list, name='check_adjudicator_list'),
    url(
        r'^(?P<tournament_id>\d+)/adjudicator/registration[/]$',
        views.registration_adjudicator,
        name='registration_adjudicator'
    ),

)
