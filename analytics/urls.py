from django.conf.urls import url
from django.urls import path

from analytics.views import index, ProfileAPI, MotionAPI

app_name = "analytics"

urlpatterns = [
    path(r'api/profile', ProfileAPI.as_view(), name='profile-api'),
    path(r'api/motion/<int:pk>/', MotionAPI.as_view(), name='motion-api'),
    path('', index, name='index'),
    path('profile/', index, name='profile'),
    path(r'motion/<int:pk>/', index, name='motion'),
    # url(r'^api/motions/', MotionList.as_view())
]
