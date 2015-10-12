__author__ = 'Alexander'

from django.shortcuts import \
    get_object_or_404, \
    render
from apps.tournament.consts import *
from apps.main.views import paging
from . models import User
from . forms import EditForm


def profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if not request.user.is_authenticated() or request.user != user:
        return show_profile(request, user)
    else:
        return edit_profile(request, user)


def show_profile(request, user):
    return render(
        request,
        'account/show.html',
        {
            'user': user,
        }
    )


def edit_profile(request, user):
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
    return paging(
        request,
        list(map(lambda x: x.tournament, user.usertournamentrel_set.filter(role=ROLE_OWNER))),
        'main/main.html'
    )

