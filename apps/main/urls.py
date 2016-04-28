from . import views
from django.conf.urls import \
    patterns, \
    url


urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^faq[/]$', views.faq, name='faq'),
    url(r'^help[/]$', views.faq, name='help'),
    url(r'^about[/]$', views.about, name='about'),
    url(r'^soon[/]$', views.soon, name='soon'),
    url(r'^news[/]$', views.news, name='news'),
    url(r'^thanks[/]$', views.thanks, name='thanks'),
)
