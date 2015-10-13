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

    url(r"^password/change/$", allauth_views.password_change, name="account_change_password"),
    url(r"^password/reset/$", allauth_views.password_reset, name="account_reset_password"),
    url(r"^password/reset/done/$", allauth_views.password_reset_done, name="account_reset_password_done"),
    url(
        r"^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$",
        allauth_views.password_reset_from_key,
        name="account_reset_password_from_key"
    ),
    url(
        r"^password/reset/key/done/$",
        allauth_views.password_reset_from_key_done,
        name="account_reset_password_from_key_done"
    ),
)
