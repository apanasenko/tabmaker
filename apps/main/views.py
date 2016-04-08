from datetime import date, timedelta
from django.shortcuts import render
from django.db.models import Count, Q
from apps.tournament.consts import *
from apps.tournament.models import Tournament
from . utils import paging


def index(request):
    DAYS_TO_LEAVE_SHORT_LIST = 3
    is_short = request.GET.get('list', None) != 'all'
    tournaments = Tournament.objects.annotate(m_count=Count('team_members')).select_related('status')
    if is_short:
        # TODO Возможно стоит всегда показывать свои турниры в списке
        tournaments = tournaments.filter(
            Q(status__in=[STATUS_STARTED, STATUS_PLAYOFF, STATUS_FINISHED])
            |
            Q(start_tour__gte=(date.today() - timedelta(days=DAYS_TO_LEAVE_SHORT_LIST)))
        )
    else:
        tournaments = tournaments.all()

    return render(
        request,
        'main/main.html',
        {
            'is_main_page': True,
            'is_short': is_short,
            'objects': paging(
                request, list(tournaments.order_by('-start_tour')), 30
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
