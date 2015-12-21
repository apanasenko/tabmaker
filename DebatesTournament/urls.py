from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'DebatesTournament.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^', include('apps.main.urls', namespace='main')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^profile/', include('apps.profile.urls')),
    url(r'^tournament/', include('apps.tournament.urls', namespace='tournament')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'', include('apps.tester.urls', namespace='tester')),
    )
