from django.conf.urls import include, url
from django.conf import settings
from django.contrib import admin
from apps.tournament.urls import main, account, tournament

urlpatterns = [
    url(r'^', include(main, namespace='main')),
    url(r'^admin/', admin.site.urls),
    url(r'^profile/', include(account)),
    url(r'^tournament/', include(tournament, namespace='tournament')),
]

if settings.TELEGRAM_BOT_ENABLE:
    from django_telegrambot import urls as django_telegrambot_urls
    urlpatterns += [
        url(r'^', include(django_telegrambot_urls)),
    ]

if settings.DEBUG:
    import debug_toolbar
    from apps.tester import urls as tester_urls
    urlpatterns += [
        url(r'', include(tester_urls, namespace='tester')),
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
