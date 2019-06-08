from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from apps.tournament.api.filters import AdjudicatorConflictFilter
from apps.tournament.api.permissions import CanEditTournamentPermission
from apps.tournament.api.serializers import ConflictSerializer
from apps.tournament.models import (
    AdjudicatorConflict)


class ConflictListCreate(generics.ListCreateAPIView):
    queryset = AdjudicatorConflict.objects.all()
    permission_classes = (CanEditTournamentPermission,)
    serializer_class = ConflictSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = AdjudicatorConflictFilter


class ConflictRUD(generics.RetrieveUpdateDestroyAPIView):
    queryset = AdjudicatorConflict.objects.all()
    permission_classes = (CanEditTournamentPermission,)
    serializer_class = ConflictSerializer
