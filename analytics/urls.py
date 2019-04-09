from django.conf.urls import url
from django.urls import path

from analytics.views import index, ProfileAPI

app_name = "analytics"

urlpatterns = [
    path(r'api/profile', ProfileAPI.as_view()),
    url('', index),
    # url(r'^api/motions/', MotionList.as_view())
]
