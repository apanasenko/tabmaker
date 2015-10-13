from django import template


register = template.Library()


@register.filter
def name(user):
    return "%s %s" % (user.first_name, user.last_name) \
        if user.last_name \
        else user.email
