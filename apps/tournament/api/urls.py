from django.urls import path

from apps.tournament.api.views import ConflictListCreate, ConflictRUD

urlpatterns = [
    path(r'conflicts/', ConflictListCreate.as_view()),
    path(r'conflict/<int:pk>/', ConflictRUD.as_view()),
]
