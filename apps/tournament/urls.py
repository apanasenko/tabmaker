from . import views
from django.conf.urls import \
    patterns, \
    url


urlpatterns = patterns(
    '',

    # Management of tournament
    url(r'^new[/]$', views.new, name='new'),
    url(r'^(?P<tournament_id>\d+)[/]$', views.show, name='show'),
    url(r'^(?P<tournament_id>\d+)/edit[/]$', views.edit, name='edit'),
    url(r'^(?P<tournament_id>\d+)/play[/]$', views.play, name='play'),
    url(r'^(?P<tournament_id>\d+)/result[/]$', views.result, name='result'),
    url(r'^(?P<tournament_id>\d+)/remove[/]$', views.remove, name='remove'),
    url(r'^(?P<tournament_id>\d+)/print[/]$', views.print_users, name='print'),

    # Change status of tournament
    url(r'^(?P<tournament_id>\d+)/registration/opening[/]$', views.registration_opening, name='registration_opening'),
    url(r'^(?P<tournament_id>\d+)/registration/closing[/]$', views.registration_closing, name='registration_closing'),
    url(r'^(?P<tournament_id>\d+)/start[/]$', views.start, name='start'),
    url(r'^(?P<tournament_id>\d+)/break[/]$', views.generate_break, name='break'),
    url(r'^(?P<tournament_id>\d+)/finished[/]$', views.finished, name='finished'),

    # Management of rounds
    url(r'^(?P<tournament_id>\d+)/round/next[/]$', views.next_round, name='next_round'),
    url(r'^(?P<tournament_id>\d+)/round/show[/]$', views.show_round, name='show_round'),
    url(r'^(?P<tournament_id>\d+)/round/presentation[/]$', views.presentation_round, name='presentation_round'),
    url(r'^(?P<tournament_id>\d+)/round/edit[/]$', views.edit_round, name='edit_round'),
    url(r'^(?P<tournament_id>\d+)/round/publish[/]$', views.publish_round, name='publish_round'),
    url(r'^(?P<tournament_id>\d+)/round/result[/]$', views.result_round, name='result_round'),
    url(r'^(?P<tournament_id>\d+)/round/remove[/]$', views.remove_round, name='remove_round'),

    # Management of teams
    url(r'^(?P<tournament_id>\d+)/team/registration[/]$', views.registration_team, name='registration_team'),
    url(r'^(?P<tournament_id>\d+)/team/add[/]$', views.add_team, name='add_team'),
    url(r'^(?P<tournament_id>\d+)/team/list[/]$', views.edit_team_list, name='edit_team_list'),
    url(r'^(?P<tournament_id>\d+)/team/check[/]$', views.edit_team_list, name='check_team_list'),
    url(r'^(?P<tournament_id>\d+)/team/edit/role[/]$', views.team_role_update, name='update_team_role'),

    # Management of adjudicator
    url(
        r'^(?P<tournament_id>\d+)/adjudicator/registration[/]$',
        views.registration_adjudicator,
        name='registration_adjudicator'
    ),
    url(r'^(?P<tournament_id>\d+)/adjudicator/add[/]$', views.add_adjudicator, name='add_adjudicator'),
    url(r'^(?P<tournament_id>\d+)/adjudicator/list[/]$', views.edit_adjudicator_list, name='edit_adjudicator_list'),
    url(r'^(?P<tournament_id>\d+)/adjudicator/check[/]$', views.edit_adjudicator_list, name='check_adjudicator_list'),
    url(
        r'^(?P<tournament_id>\d+)/adjudicator/edit/role[/]$',
        views.adjudicator_role_update,
        name='update_adjudicator_role'
    ),
)
