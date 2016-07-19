from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Q
from django.http import Http404
from django.shortcuts import \
    get_object_or_404, \
    render
from django.views.decorators.csrf import ensure_csrf_cookie

from apps.tournament.consts import *
from apps.tournament.forms_profile import EditForm
from apps.tournament.models import Tournament, TeamTournamentRel
from apps.tournament.models import User
from apps.tournament.utils import paging


def show_profile(request, user_id):

    try:
        # not use get_object_or_404 because need select_related
        users = User.objects
        for name in ['university', 'university__city', 'university__country']:
            users = users.select_related(name)
        user = users.get(pk=user_id)
    except ObjectDoesNotExist:
        raise Http404('User with id %d not exist' % user_id)

    teams_rel = TeamTournamentRel.objects.filter(Q(team__speaker_1=user) | Q(team__speaker_2=user))
    for name in ['role', 'team__speaker_2', 'team__speaker_1', 'tournament']:
        teams_rel = teams_rel.select_related(name)

    adjudicators_rel = user.usertournamentrel_set.filter(role__in=ADJUDICATOR_ROLES)
    for name in ['role', 'tournament']:
        adjudicators_rel = adjudicators_rel.select_related(name)

    return render(
        request,
        'account/show.html',
        {
            'user': user,
            'is_owner': request.user.is_authenticated() and user == request.user,
            'teams_objects': teams_rel,
            'adjudicators_objects': adjudicators_rel,
        }
    )


def edit_profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if not request.user.is_authenticated() or request.user != user:
        raise Http404
    is_success = False
    if request.method == 'POST':
        form = EditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            is_success = True
    else:
        form = EditForm(instance=user)
    return render(
        request,
        'account/signup.html',
        {
            'is_edit_form': True,
            'is_success': is_success,
            'user': user,
            'form': form,
        }
    )


def show_tournaments_of_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    tournaments = Tournament.objects.annotate(
        m_count=Count('team_members')
    ).select_related('status').filter(
        usertournamentrel__user=user, usertournamentrel__role__in=[ROLE_ADMIN, ROLE_OWNER]
    ).order_by('-start_tour')

    return render(
        request,
        'main/main.html',
        {
            'is_main_page': False,
            'is_owner': request.user == user,
            'objects': paging(request, tournaments)
        }
    )


@ensure_csrf_cookie
def show_teams_of_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    teams_rel = TeamTournamentRel.objects.filter(Q(team__speaker_1=user) | Q(team__speaker_2=user))
    for name in ['role', 'team__speaker_2', 'team__speaker_1', 'tournament']:
        teams_rel = teams_rel.select_related(name)
    return render(
        request,
        'account/teams_of_user.html',
        {
            'is_owner': request.user == user,
            'objects': paging(
                request,
                teams_rel
            )
        }
    )


@ensure_csrf_cookie
def show_adjudicator_of_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    adjudicators_rel = user.usertournamentrel_set.filter(role__in=ADJUDICATOR_ROLES)
    for name in ['role', 'tournament']:
        adjudicators_rel = adjudicators_rel.select_related(name)

    return render(
        request,
        'account/adjudicators_of_user.html',
        {
            'is_owner': request.user == user,
            'objects': paging(
                request,
                adjudicators_rel,
            )
        }
    )
