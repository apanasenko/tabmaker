from django.conf.urls import \
    patterns, \
    url
from . import views


urlpatterns = patterns(
    "",
    url(r"^(?P<user_id>\d+)[/]$", views.profile, name='main'),
    url(r"^(?P<user_id>\d+)/tournaments[/]", views.show_tournaments_of_user, name='tournaments'),
)

