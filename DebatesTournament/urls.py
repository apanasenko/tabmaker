from django.conf.urls import include, url
from django.conf import settings
from django.contrib import admin


urlpatterns = [
    url(r'^', include('apps.tournament.urls.main', namespace='main')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^profile/', include('apps.tournament.urls.account')),
    url(r'^tournament/', include('apps.tournament.urls.tournament', namespace='tournament')),
]
