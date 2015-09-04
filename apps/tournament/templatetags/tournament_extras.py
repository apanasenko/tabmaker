__author__ = 'Alexander'

from django import template


register = template.Library()


@register.filter
def registered_users(tournament):
    return "%s" % tournament.team_members.count()


@register.filter
def address(tournament):
    lines = tournament.location.split(', ')
    if len(lines) > 2:
        return "%s, %s" % (lines[0], lines[1])
    return tournament.location
