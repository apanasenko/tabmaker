__author__ = 'Alexander'

from django import template


register = template.Library()


@register.filter
def registered_users(tournament):
    return "%s" % tournament.team_members.count()
