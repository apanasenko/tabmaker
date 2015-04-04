from django.shortcuts import render
from apps.tournament.models import Tournament


def index(request):
    return render(request, 'main/base.html', {'tournaments': Tournament.objects.all()})
