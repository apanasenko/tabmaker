import os
from collections import defaultdict

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from DebatesTournament.settings import BASE_DIR, DEBUG
from analytics.caching import cache_wrapper
from analytics.filters import MotionAnalysisFilter
from analytics.serializers import MotionSerializer, UserSerializer
from apps.tournament.models import Motion, Team, QualificationResult, Game


def index(request):
    if DEBUG:
        return render(request, 'index.html')
    try:
        with open(os.path.join(BASE_DIR, 'frontend', 'build', 'index.html')) as f:
            return HttpResponse(f.read())
    except FileNotFoundError:
        return HttpResponse(
            """
            This URL is only used when you have built the production
            version of the app. Visit http://localhost:3000/ instead, or
            run `yarn run build` to test the production version.
            """,
            status=501,
        )


class ProfileAPI(APIView):
    # TODO: count only finished tournaments
    # TODO: add judging stats
    # TODO: add cache
    # TODO: add user as param
    renderer_classes = (JSONRenderer,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        # user = User.objects.get(id=50)
        teams = Team.objects.filter(
            Q(speaker_1=user.id) | Q(speaker_2=user.id)
        ).prefetch_related(
            'OG', 'OG__game', 'OG__game__gameresult', 'OG__game__gameresult__qualificationresult',
            'OO', 'OO__game', 'OO__game__gameresult', 'OO__game__gameresult__qualificationresult',
            'CG', 'CG__game', 'CG__game__gameresult', 'CG__game__gameresult__qualificationresult',
            'CO', 'CO__game', 'CO__game__gameresult', 'CO__game__gameresult__qualificationresult',
        )
        results = QualificationResult.objects.filter(
            Q(game__og__speaker_1=user.id) | Q(game__og__speaker_2=user.id) |
            Q(game__oo__speaker_1=user.id) | Q(game__oo__speaker_2=user.id) |
            Q(game__co__speaker_1=user.id) | Q(game__co__speaker_2=user.id) |
            Q(game__cg__speaker_1=user.id) | Q(game__cg__speaker_2=user.id)) \
            .select_related(
            'game', 'game__og', 'game__oo', 'game__co', 'game__cg'
        ).order_by('id')
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
            is_reversed = getattr(res, f'{position}_rev')
            spkr = 0
            if position == 'og':
                spkr = res.pm if registered_as_first and not is_reversed else res.dpm
            if position == 'oo':
                spkr = res.lo if registered_as_first and not is_reversed else res.dlo
            if position == 'cg':
                spkr = res.mg if registered_as_first and not is_reversed else res.gw
            if position == 'co':
                spkr = res.mo if registered_as_first and not is_reversed else res.ow
            answer[position].append((getattr(res, position), spkr))
            answer['overall'].append((getattr(res, position), spkr))

        judgement = list(Game.objects.filter(chair=user))
        answer['judgement'] = len(judgement)
        user.analytics = answer
        serializer = UserSerializer(user)
        return Response(serializer.data)


cached_profile = cache_wrapper(ProfileAPI.as_view())


class MotionList(generics.ListAPIView):
    queryset = Motion.objects.all().select_related('analysis')
    serializer_class = MotionSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = MotionAnalysisFilter
