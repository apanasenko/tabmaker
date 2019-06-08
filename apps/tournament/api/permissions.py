from rest_framework import permissions
from rest_framework.request import Request

from apps.tournament.logic import user_can_edit_tournament
from apps.tournament.models import Tournament


class CanEditTournamentPermission(permissions.BasePermission):
    def has_object_permission(self, request: Request, view, obj):
        user = request.user
        if not user.is_authenticated:
            return False
        tournament = Tournament.objects.get(id=request.data['tournament'])
        return user_can_edit_tournament(tournament, user)
