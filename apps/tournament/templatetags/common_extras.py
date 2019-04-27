from django import template

register = template.Library()

@register.filter
def index(dictionary, name):
    return dictionary.get(name, 0)
