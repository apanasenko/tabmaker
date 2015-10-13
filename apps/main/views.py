from django.shortcuts import render
from apps.tournament.models import Tournament
from . utils import paging


def index(request):
    return render(
        request,
        'main/main.html',
        {
            'objects': paging(request, Tournament.objects.all())
        }
    )
