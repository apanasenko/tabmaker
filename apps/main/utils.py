from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def debug_mode(request):
    from django.conf import settings
    return {
        'debug': settings.DEBUG,
        'template_debug': settings.TEMPLATE_DEBUG
    }


def paging(request, objects, count_objects_in_page=5):
    paginator = Paginator(objects, count_objects_in_page)
    page = request.GET.get('page')
    try:
        objects_in_page = paginator.page(page)
    except PageNotAnInteger:
        objects_in_page = paginator.page(1)
    except EmptyPage:
        objects_in_page = paginator.page(paginator.num_pages)

    return objects_in_page
