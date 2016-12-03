from . import views
from django.conf.urls import url


urlpatterns = [
    url(
        r'^generate/(?P<tournament_id>\d+)/results[/]$',
        views.generate_results
    ),
    url(
        r'^generate/(?P<tournament_id>\d+)/place/(?P<count>\d+)[/]$',
        views.generate_places
    ),
    url(
        r'^generate/(?P<tournament_id>\d+)/(?P<func>(team|adjudicator))/(?P<role_id>\d+)/(?P<count>\d+)[/]$',
        views.generate
    ),
    url(
        r'^remove/(?P<actor>(team|user))/(?P<id>\d+)[/]$',
        views.remove
    ),
    url(
        r'^clone/tournament/(?P<count>\d+)[/]$',
        views.clone_tournament
    ),
    url(
        r'^restart/(?P<tournament_id>\d+)[/]$',
        views.restart_tournament
    ),
]
