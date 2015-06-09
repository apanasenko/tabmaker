__author__ = 'Alexander'


def debug_mode(request):
    from django.conf import settings
    return {
        'debug': settings.DEBUG,
        'template_debug': settings.TEMPLATE_DEBUG
    }
