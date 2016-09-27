from django import template

COUNT_PAGE_SHOW = 3
register = template.Library()


@register.filter
def is_split_first(number):
    return number - COUNT_PAGE_SHOW > 2


@register.filter
def page_range(number):
    return range(number - COUNT_PAGE_SHOW, number + COUNT_PAGE_SHOW)
