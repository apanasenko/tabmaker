__author__ = 'Alexander'

from django.shortcuts import \
    get_object_or_404, \
    render
from . models import User


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
    # if request.method == 'POST':
    #     pass
    # else:
    #     form = ProfileForm(instance=user)
    # TODO Редактирование профиля
    return render(
        request,
        'account/show.html',
        {
            'user': user,
        }
    )

