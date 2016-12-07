from allauth.account import urls as allauth_urls
from allauth.socialaccount.providers.google.urls import urlpatterns as google_urlpatterns
# from allauth.socialaccount.providers.mailru.urls import urlpatterns as mailru_urlpatterns
from allauth.socialaccount.urls import urlpatterns as socialaccount_urlpatterns
from django.conf.urls import url, include


urlpatterns = [
    url(r"^", include('apps.tournament.urls.profile', namespace='profile')),
    url(r"^", include(allauth_urls)),
    # TODO url(r"^password/set/$", views.password_set, name="account_set_password"),
    # TODO url(r"^inactive/$", views.account_inactive, name="account_inactive"),
    # TODO url(r"^email/$", views.email, name="account_email"),
]

urlpatterns += google_urlpatterns
# urlpatterns += mailru_urlpatterns
urlpatterns += socialaccount_urlpatterns
