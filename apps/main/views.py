from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from apps.tournament.models import Tournament


def index(request):
    return paging(request, Tournament.objects.all(), 'main/main.html')


def paging(request, objects, page_name, count_objects_in_page=10):
    paginator = Paginator(objects, count_objects_in_page)
    page = request.GET.get('page')
    try:
        objects_in_page = paginator.page(page)
    except PageNotAnInteger:
        objects_in_page = paginator.page(1)
    except EmptyPage:
        objects_in_page = paginator.page(paginator.num_pages)

    return render(request, page_name, {'objects': objects_in_page})
