from django.conf.urls import \
    patterns, \
    url

from apps.tournament import utils_profile, views_profile

urlpatterns = patterns(
    "",
    url(r"^(?P<user_id>\d+)[/]$", views_profile.show_profile, name='main'),
    url(r"^(?P<user_id>\d+)/edit[/]$", views_profile.edit_profile, name='edit'),
    url(r"^(?P<user_id>\d+)/tournaments[/]$", views_profile.show_tournaments_of_user, name='tournaments'),
    url(r"^(?P<user_id>\d+)/teams[/]$", views_profile.show_teams_of_user, name='teams'),
    url(r"^(?P<user_id>\d+)/adjudicator[/]$", views_profile.show_adjudicator_of_user, name='adjudicator'),

    url(r"^team/remove[/]$", utils_profile.team_remove, name='team_remove'),
    url(r"^adjudicator/remove[/]$", utils_profile.adjudicator_remove, name='adjudicator_remove'),
)

