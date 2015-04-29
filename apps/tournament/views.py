import datetime
import pytz
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from apps.team.forms import TeamRegistrationForm
from .forms import \
    TournamentForm, \
    TeamRoleForm
from .consts import *
from .models import \
    Tournament,\
    TeamTournamentRel,\
    UserTournamentRel


def index(request):
    # TODO придумать зачем эта страница
    return show_message(request, 'Нужна ди эта страница?')


@login_required(login_url=reverse_lazy('account_login'))
def new(request):
    if request.method == 'POST':
        tournament_form = TournamentForm(request.POST)
        if tournament_form.is_valid():
            tournament_obj = tournament_form.save(commit=False)
            tournament_obj.count_rounds = 0
            tournament_obj.save()
            UserTournamentRel.objects.create(
                user=request.user,
                tournament=tournament_obj,
                role=ROLE_OWNER
            )

            # TODO куда перекидывать
            return show_message(request, 'Вы создали свой турнир')

    else:
        tournament_form = TournamentForm()

    return render(request, 'tournament/new.html', {'form': tournament_form})


def show(request, tournament_id):
    tournament = get_object_or_404(Tournament, pk=tournament_id)

    return render(
        request,
        'tournament/show.html',
        {
            'tournament': tournament,
            'is_owner': user_can_edit_tournament(tournament, request.user)
        }
    )


@login_required(login_url=reverse_lazy('account_login'))
def edit(request, tournament_id):
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    if not user_can_edit_tournament(tournament, request.user):
        # TODO страница ошибки доступа
        return show_message(request, 'У вас нет прав для редактирования турнира')

    if request.method == 'POST':
        tournament_form = TournamentForm(request.POST, instance=tournament)
        if tournament_form.is_valid():
            tournament_form.save()

            return show_message(request, 'Турнир изменён')

    else:
        tournament_form = TournamentForm(instance=tournament)

    return render(
        request,
        'tournament/edit.html',
        {
            'form': tournament_form,
            'id': tournament.id,
        }
    )


@login_required(login_url=reverse_lazy('account_login'))
def registration_team(request, tournament_id):
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    if not tournament.open_reg < datetime.datetime.now(tz=pytz.utc) < tournament.close_reg:
        return show_message(request, 'Регистрация уже (ещё) закрыта ((')

    if request.method == 'POST':
        team_form = TeamRegistrationForm(request.POST)
        if team_form.is_valid():
            team_obj = team_form.save(commit=False)
            team_obj.speaker_1 = request.user
            team_obj.speaker_2 = User.objects.get(email=team_form.cleaned_data['speaker_2'])
            team_obj.save()
            TeamTournamentRel.objects.create(
                team=team_obj,
                tournament=tournament,
                role=ROLE_TEAM_REGISTERED
            )

            return show_message(request, 'Вы успешно зарегались в %s' % tournament.name)

    else:
        team_form = TeamRegistrationForm(initial={'speaker_1': request.user.email})

    return render(
        request,
        'tournament/registration.html',
        {
            'form': team_form,
            'id': tournament_id,
            'user': request.user,
        }
    )


@login_required(login_url=reverse_lazy('account_login'))
def registration_adjudicator(request, tournament_id):
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    if not tournament.open_reg < datetime.datetime.now(tz=pytz.utc) < tournament.close_reg:
        return show_message(request, 'Регистрация уже (ещё) закрыта ((')

    # TODO: Добавить проверку уже зареганного судьи
    UserTournamentRel.objects.create(
        user=request.user,
        tournament=tournament,
        role=ROLE_ADJUDICATOR_REGISTERED[0]
    )
    return show_message(request, 'Вы успешно зарегались в %s как судья' % tournament.name)


def show_team_list(request, tournament_id):
    tournament = get_object_or_404(Tournament, pk=tournament_id)

    return render(
        request,
        'tournament/teamList.html',
        {
            'teams': tournament.team_members.all(),
        }
    )


def edit_team_list(request, tournament_id):
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    forms = []
    for team_rel in tournament.teamtournamentrel_set.all().order_by('team_id'):
        if request.method == 'POST':
            team = TeamRoleForm(request.POST, instance=team_rel, prefix=team_rel.team.id)
            if team.is_valid():
                team.save()

        team = team_rel.team
        form = TeamRoleForm(instance=team_rel, prefix=team.id)
        forms.append({
            'team': team,
            'team_form': form
        })

    return render(
        request,
        'tournament/edit_team_list.html',
        {
            'forms': forms,
            'id': tournament_id,
        }
    )


def show_adjudicator_list(request, tournament_id):
    tournament = get_object_or_404(Tournament, pk=tournament_id)

    return render(
        request,
        'tournament/adjudicatorList.html',
        {
            'adjudicators': tournament.usertournamentrel_set.filter(
                role_id__in=[
                    ROLE_ADJUDICATOR_REGISTERED[0],  # TODO Разобраться, почему тут приходит картеж
                ]
            ),
        }
    )


def user_can_edit_tournament(t: Tournament, u: User):
    # TODO добавить админов
    return u.is_authenticated() and 0 < len(UserTournamentRel.objects.filter(
        tournament=t,
        user=u,
        role=ROLE_OWNER
    ))


def show_message(request, message):
    return render(request, 'main/message.html', {'message': message})
