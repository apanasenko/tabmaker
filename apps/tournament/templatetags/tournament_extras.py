__author__ = 'Alexander'

from django import template
from ..consts import *


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


@register.filter
def is_status_registration(tournament):
    return tournament.status == STATUS_REGISTRATION


@register.filter
def is_status_preparation(tournament):
    return tournament.status == STATUS_PREPARATION


@register.filter
def is_status_started(tournament):
    return tournament.status == STATUS_STARTED


@register.filter
def is_status_playoff(tournament):
    return tournament.status == STATUS_PLAYOFF


@register.filter
def is_status_finished(tournament):
    return tournament.status == STATUS_FINISHED
