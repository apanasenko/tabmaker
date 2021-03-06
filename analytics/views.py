import json
from collections import defaultdict

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy, get_resolver
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from analytics.filters import MotionAnalysisFilter
from analytics.models import MotionAnalysis
from analytics.serializers import (
    MotionSerializer, UserAnalyticsSerializer, DefaultUserSerializer
)
from apps.tournament.consts import STATUS_FINISHED
from apps.tournament.models import (
    Motion, QualificationResult, Game, User
)


@login_required(login_url=reverse_lazy('account_login'))
def index(request, *args, **kwargs):
    user = User.objects.get(pk=request.user.id)
    user_data = json.dumps(DefaultUserSerializer(instance=user).data)
    render_data = dict(
        user_data=user_data,
    )
    return render(request, 'index.html', context=render_data)


class ProfileAPI(APIView):
    # TODO: add cache
    # TODO: add user as param
    renderer_classes = (JSONRenderer,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        results = QualificationResult.objects.filter(
            Q(game__og__speaker_1=user.id) | Q(game__og__speaker_2=user.id)
            | Q(game__oo__speaker_1=user.id) | Q(game__oo__speaker_2=user.id)
            | Q(game__co__speaker_1=user.id) | Q(game__co__speaker_2=user.id)
            | Q(game__cg__speaker_1=user.id) | Q(game__cg__speaker_2=user.id)) \
            .select_related(
            'game', 'game__og', 'game__oo', 'game__co', 'game__cg'
        ).order_by('id').filter(
            game__motion__round__tournament__status_id=STATUS_FINISHED
        )
        answer = defaultdict(list)
        for res in results:
            position = ''
            if user in (res.game.og.speaker_2, res.game.og.speaker_1):
                position = 'og'
            if user in (res.game.oo.speaker_2, res.game.oo.speaker_1):
                position = 'oo'
            if user in (res.game.cg.speaker_2, res.game.cg.speaker_1):
                position = 'cg'
            if user in (res.game.co.speaker_2, res.game.co.speaker_1):
                position = 'co'
            registered_as_first = getattr(res.game, position).speaker_1 == user
            speaks = 0
            if position == 'og':
                speaks = res.pm if registered_as_first else res.dpm
            if position == 'oo':
                speaks = res.lo if registered_as_first else res.dlo
            if position == 'cg':
                speaks = res.mg if registered_as_first else res.gw
            if position == 'co':
                speaks = res.mo if registered_as_first else res.ow
            answer[position].append((getattr(res, position), speaks))
            answer['overall'].append((getattr(res, position), speaks))

        judgement = list(Game.objects.filter(chair=user))
        answer['judgement'] = len(judgement)
        user.analytics = answer
        serializer = UserAnalyticsSerializer(user)
        return Response(serializer.data)


# TODO: add proper signal to models to make this thing available again
# cached_profile = cache_wrapper(ProfileAPI.as_view())

class MotionAPI(APIView):
    queryset = Motion.objects.select_related('analysis') \
            .filter(round__tournament__status_id=STATUS_FINISHED)

    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']
        try:
            motion = self.queryset.get(id=pk)
        except Motion.DoesNotExist:
            motion = None
        if not motion:
            return Response(status=200, data={})
        if not hasattr(motion, 'analysis'):
            analysis = MotionAnalysis()
            analysis.generate_analysis(motion)
            motion.analysis = analysis
        data = MotionSerializer(motion).data
        return Response(status=200, data=data)


class MotionList(generics.ListAPIView):
    queryset = Motion.objects.all().select_related('analysis')
    serializer_class = MotionSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = MotionAnalysisFilter
