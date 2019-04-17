from rest_framework import serializers

from analytics.models import MotionAnalysis
from apps.tournament.models import Motion, User


class MotionAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = MotionAnalysis
        fields = '__all__'


class MotionSerializer(serializers.ModelSerializer):
    analysis = MotionAnalysisSerializer(read_only=True)

    class Meta:
        model = Motion
        fields = '__all__'


class DefaultUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'university']


class UserAnalyticsSerializer(serializers.ModelSerializer):
    analytics = serializers.JSONField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'analytics', ]
