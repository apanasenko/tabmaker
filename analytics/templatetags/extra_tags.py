from django import template
from django.conf import settings
from django.template.defaultfilters import urlencode

from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.templatetags.static import static
from django.contrib.staticfiles import finders

register = template.Library()


@register.simple_tag
def hmr_script(path):
    script_origin = ''
    if settings.DEBUG and settings.WEBPACK_DEV_SERVER:
        script_origin = f'http://{settings.WEBPACK_DEV_SERVER}'

    return format_html(
        mark_safe('<script type="text/javascript" src="{}{}"></script>'),
        script_origin,
        path
    )

@register.simple_tag
def existing_style(path, **kwargs):
    if not finders.find(path):
        return ''

    return format_html(
        mark_safe('<link rel="stylesheet" type="text/css" href="{}?{}" />'),
        path, urlencode(kwargs))
