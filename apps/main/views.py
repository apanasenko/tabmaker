from datetime import date, timedelta
from django.shortcuts import render
from django.db.models import Count, Q
from apps.tournament.consts import *
from apps.tournament.models import Tournament
from . utils import paging


def index(request):
    DAYS_TO_LEAVE_SHORT_LIST = 7
    is_short = request.GET.get('list', None) != 'all'
    if is_short:
        if request.user.is_authenticated():
            self_tournament = (
                Q(usertournamentrel__user=request.user) & Q(usertournamentrel__role__in=[ROLE_ADMIN, ROLE_OWNER])
            )
        else:
            self_tournament = ~Q()

        tournaments = Tournament.objects.annotate(m_count=Count('team_members')).filter(
            Q(m_count__gt=0)
            | (Q(status=STATUS_REGISTRATION)
                & Q(start_tour__gte=(date.today() - timedelta(days=DAYS_TO_LEAVE_SHORT_LIST))))
            | self_tournament
        ).distinct()

    else:
        tournaments = Tournament.objects.all()

    return render(
        request,
        'main/main.html',
        {
            'is_main_page': True,
            'is_short': is_short,
            'objects': paging(
                request, tournaments.order_by('-start_tour'), 30
            )
        }
    )


def faq(request):
    return render(
        request,
        'main/intro.html'
    )


def about(request):
    return render(
        request,
        'main/about.html'
    )


def soon(request):
    return render(
        request,
        'main/soon.html'
    )


def news(request):
    return render(
        request,
        'main/news.html'
    )
