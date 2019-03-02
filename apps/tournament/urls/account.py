from allauth.account.urls import urlpatterns as allauth_urls
from allauth.socialaccount.providers.google.urls import urlpatterns as google_urlpatterns
from allauth.socialaccount.providers.mailru.urls import urlpatterns as mailru_urlpatterns
from allauth.socialaccount.providers.vk.urls import urlpatterns as vk_urlpatterns
from allauth.socialaccount.providers.facebook.urls import urlpatterns as facebook_urlpatterns
from allauth.socialaccount.urls import urlpatterns as socialaccount_urlpatterns
from django.conf.urls import url, include
from apps.tournament.urls import profile as profile_url


urlpatterns = [
    url(r"^", include(profile_url, namespace='profile')),
]

urlpatterns += allauth_urls
# TODO url(r"^password/set/$", views.password_set, name="account_set_password"),
# TODO url(r"^inactive/$", views.account_inactive, name="account_inactive"),
# TODO url(r"^email/$", views.email, name="account_email"),
urlpatterns += google_urlpatterns
urlpatterns += mailru_urlpatterns
urlpatterns += vk_urlpatterns
urlpatterns += facebook_urlpatterns
urlpatterns += socialaccount_urlpatterns
# TODO url('^signup/$', views.signup, name='socialaccount_signup'),
# TODO url('^connections/$', views.connections, name='socialaccount_connections')
