from django.shortcuts import \
    get_object_or_404, \
    render
from django.http import Http404
from apps.tournament.consts import *
from apps.main.utils import paging
from . models import User
from . forms import EditForm
from django.views.decorators.csrf import ensure_csrf_cookie


def show_profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    return render(
        request,
        'account/show.html',
        {
            'user': user,
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
    return render(
        request,
        'main/main.html',
        {
            'is_owner': request.user == user,
            'objects': paging(
                request,
                list(map(lambda x: x.tournament, user.usertournamentrel_set.filter(role=ROLE_OWNER)))
            )
        }
    )


@ensure_csrf_cookie
def show_teams_of_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    teams = list(user.first_speaker.all()) + list(user.second_speaker.all())
    return render(
        request,
        'account/teams_of_user.html',
        {
            'is_owner': request.user == user,
            'objects': paging(
                request,
                list(map(lambda x: {'team': x, 'rel': x.teamtournamentrel_set.first()}, teams))
            )
        }
    )


@ensure_csrf_cookie
def show_adjudicator_of_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    return render(
        request,
        'account/adjudicators_of_user.html',
        {
            'is_owner': request.user == user,
            'objects': paging(
                request,
                user.usertournamentrel_set.filter(role__in=ADJUDICATOR_ROLES),
            )
        }
    )
