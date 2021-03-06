from apps.tournament import views
from django.conf.urls import url


app_name = 'tournament'
urlpatterns = [

    # Management of tournament
    url(r'^new[/]$', views.new, name='new'),
    url(r'^(?P<tournament_id>\d+)[/]$', views.show, name='show'),
    url(r'^(?P<tournament_id>\d+)/new[/]$', views.created, name='created'),
    url(r'^(?P<tournament_id>\d+)/edit[/]$', views.edit, name='edit'),
    url(r'^(?P<tournament_id>\d+)/result[/]$', views.result, name='result'),
    url(r'^(?P<tournament_id>\d+)/result/all[/]$', views.result_all_rounds, name='result_all'),
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
    url(r'^(?P<tournament_id>\d+)/team/import[/]$', views.import_team, name='import_team'),
    url(r'^(?P<tournament_id>\d+)/team/add[/]$', views.add_team, name='add_team'),
    url(r'^(?P<tournament_id>\d+)/team/list[/]$', views.edit_team_list, name='edit_team_list'),
    url(r'^(?P<tournament_id>\d+)/team/check[/]$', views.edit_team_list, name='check_team_list'),
    url(r'^(?P<tournament_id>\d+)/team/edit/role[/]$', views.team_role_update, name='update_team_role'),
    url(r'^(?P<tournament_id>\d+)/team/feedback[/]$', views.team_feedback, name='team_feedback'),

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

    # Management of admin
    url(r'^(?P<tournament_id>\d+)/admin/edit[/]$', views.list_admin, name='admin_list'),
    url(r'^(?P<tournament_id>\d+)/admin/add[/]$', views.add_admin, name='admin_add'),
    url(r'^(?P<tournament_id>\d+)/admin/remove[/]$', views.remove_admin, name='admin_remove'),
    url(r'^(?P<tournament_id>\d+)/owner/change[/]$', views.change_owner, name='owner_change'),

    # Places
    url(r'^(?P<tournament_id>\d+)/place/edit[/]', views.place_list, name='place_list'),
    url(r'^(?P<tournament_id>\d+)/place/check[/]', views.place_list, name='place_check'),
    url(r'^(?P<tournament_id>\d+)/place/add[/]', views.place_add, name='place_add'),
    url(r'^(?P<tournament_id>\d+)/place/remove[/]', views.place_remove, name='place_remove'),
    url(r'^(?P<tournament_id>\d+)/place/update[/]', views.place_update, name='place_update'),

    # Custom form
    url(
        r'^(?P<tournament_id>\d+)/(?P<form_type>(team|feedback|adjudicator|audience))/form[/]$',
        views.custom_form_edit,
        name='custom_form_edit'
    ),
    url(
        r'^(?P<tournament_id>\d+)/form/edit[/]$',
        views.custom_form_edit_field,
        name='custom_form_edit_field'
    ),
    url(
        r'^(?P<tournament_id>\d+)/(?P<form_type>(team|feedback|adjudicator|audience))/form/answers[/]$',
        views.custom_form_show_answers,
        name='custom_form_answers'
    ),
]
