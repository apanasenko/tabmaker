from django.conf.urls import url
from django.urls import path

from analytics.views import index, ProfileAPI, MotionAPI

app_name = "analytics"

urlpatterns = [
    path(r'api/profile', ProfileAPI.as_view()),
    path(r'api/motion/<int:pk>/', MotionAPI.as_view()),
    url(r'', index),
]
