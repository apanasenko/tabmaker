__author__ = 'Alexander'

from django.conf.urls import patterns, url
from apps.main import views


urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
)
