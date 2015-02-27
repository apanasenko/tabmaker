from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'DebatesTournament.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'apps.main.views.index', name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^tournament/', include('apps.tournament.urls', namespace='tournament')),
)
