from rest_framework import serializers

from apps.tournament.models import AdjudicatorConflict, Tournament, User, Team
from utils.ModelSerializerWithExtraFields import ModelSerializerWithExtraFields


class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'


class ConflictSerializer(ModelSerializerWithExtraFields):
    tournament_info = TournamentSerializer(read_only=True)
    adjudicator_info = UserSerializer(read_only=True)
    team_info = TeamSerializer(read_only=True)

    class Meta:
        model = AdjudicatorConflict
        fields = '__all__'
