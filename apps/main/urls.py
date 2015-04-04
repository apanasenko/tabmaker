__author__ = 'Alexander'

from . import views
from django.conf.urls import \
    patterns, \
    url


urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
)
