from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from apps.tournament.models import Tournament


def index(request):
    paginator = Paginator(Tournament.objects.all(), 10)
    page = request.GET.get('page')
    try:
        tournaments = paginator.page(page)
    except PageNotAnInteger:
        tournaments = paginator.page(1)
    except EmptyPage:
        tournaments = paginator.page(paginator.num_pages)

    return render(request, 'main/main.html', {'tournaments': tournaments})
