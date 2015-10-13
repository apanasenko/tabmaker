from django.conf.urls import \
    patterns, \
    url
from . import views


urlpatterns = patterns(
    "",
    url(r"^(?P<user_id>\d+)[/]$", views.show_profile, name='main'),
    url(r"^(?P<user_id>\d+)/edit[/]$", views.edit_profile, name='edit'),
    url(r"^(?P<user_id>\d+)/tournaments[/]", views.show_tournaments_of_user, name='tournaments'),
    url(r"^(?P<user_id>\d+)/teams[/]", views.show_teams_of_user, name='teams'),
    url(r"^(?P<user_id>\d+)/adjudicator[/]", views.show_adjudicator_of_user, name='adjudicator'),
)

