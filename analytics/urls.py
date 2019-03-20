from django.conf.urls import url
from django.urls import path

from analytics.views import index, MotionList, ProfileAPI, cached_profile

app_name = "analytics"

urlpatterns = [
    path(r'', index),
    path(r'api/profile', cached_profile),
    # url(r'^api/motions/', MotionList.as_view())
]
