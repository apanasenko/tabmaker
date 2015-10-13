__author__ = 'Alexander'

from allauth.account import views as allauth_views
from django.views.generic import RedirectView
from django.conf.urls import \
    patterns, \
    url, \
    include


urlpatterns = patterns(
    "",
    url(r"^", include('apps.profile.urls_profile', namespace='profile')),
    url(r"^signup/$", allauth_views.signup, name="account_signup"),
    url(r"^login/$", allauth_views.login, name="account_login"),
    url(r"^logout/$", allauth_views.logout, name="account_logout"),

    url(r"^confirm-email/$", allauth_views.email_verification_sent, name="account_email_verification_sent"),
    url(r"^confirm-email/(?P<key>\w+)/$", allauth_views.confirm_email, name="account_confirm_email"),
    # Handle old redirects
    url(r"^confirm_email/(?P<key>\w+)/$", RedirectView.as_view(url='/accounts/confirm-email/%(key)s/', permanent=True)),
)
