from django.shortcuts import render
from apps.tournament.models import Tournament
from . utils import paging


def index(request):
    return render(
        request,
        'main/main.html',
        {
            'objects': paging(request, Tournament.objects.all().order_by('-start_tour'))
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
