import datetime
import pytz
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import \
    reverse_lazy, \
    reverse
from django.shortcuts import \
    render, \
    get_object_or_404, \
    redirect

from apps.profile.models import User
from apps.team.forms import TeamRegistrationForm
from apps.motion.forms import MotionForm
from apps.game.forms import \
    GameForm, \
    ResultGameForm

from .forms import \
    TournamentForm, \
    TeamRoleForm, \
    UserRoleForm, \
    RoundForm

from .consts import *
from .models import \
    Tournament,\
    TeamTournamentRel,\
    UserTournamentRel

from .logic import \
    get_or_generate_next_round, \
    get_last_round_games_and_results, \
    remove_last_round


def index(request):
    # TODO придумать зачем эта страница
    return show_message(request, 'Нужна ди эта страница?')


@login_required(login_url=reverse_lazy('account_login'))
def new(request):
    if request.method == 'POST':
        tournament_form = TournamentForm(request.POST)
        if tournament_form.is_valid():
            tournament_obj = tournament_form.save(commit=False)
            tournament_obj.status = STATUS_REGISTRATION
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
def play(request, tournament_id):
    tournament = get_object_or_404(Tournament, pk=tournament_id)

    return render(
        request,
        'tournament/play.html',
        {
            'tournament': tournament,
        }
    )


@login_required(login_url=reverse_lazy('account_login'))
def next_round(request, tournament_id):
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    # TODO Проверить статус турнира и выводить норм инфу
    # if tournament.status != STATUS_STARTED:
    #     return show_message(request, 'Проверте статус турнира, от должен быть "started"')

    if request.method == 'POST':
        motion_form = MotionForm(request.POST)
        round_form = RoundForm(request.POST)
        if motion_form.is_valid() and round_form.is_valid():
            round_obj = round_form.save(commit=False)
            round_obj.tournament = tournament
            round_obj.number = tournament.round_number_inc()
            round_obj.motion = motion_form.save()
            round_obj.save()
            return redirect('tournament:edit_round', tournament_id=tournament_id)
    else:
        motion_form = MotionForm()
        round_form = RoundForm()

    return render(
        request,
        'tournament/next_round.html',
        {
            'tournament_id': tournament_id,
            'motion_form': motion_form,
            'round_form': round_form,
        }
    )


@login_required(login_url=reverse_lazy('account_login'))
def edit_round(request, tournament_id):
    tournament = get_object_or_404(Tournament, pk=tournament_id)

    forms = []
    all_is_valid = True
    for room in get_or_generate_next_round(tournament):
        if request.method == 'POST':
            form = GameForm(request.POST, instance=room.game, prefix=room.game.id)
            all_is_valid &= form.is_valid()
            if form.is_valid():
                form.save()
        else:
            form = GameForm(instance=room.game, prefix=room.game.id)

        # TODO Добавить название в команд в форму и не передавать объект
        forms.append({
            'game': room.game,
            'game_form': form
        })

    if all_is_valid and request.method == 'POST':
        return redirect('tournament:play', tournament_id=tournament_id)

    return render(
        request,
        'tournament/edit_round.html',
        {
            'tournament': tournament,
            'forms': forms,
        }
    )


@login_required(login_url=reverse_lazy('account_login'))
def result_round(request, tournament_id):
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    all_is_valid = True
    forms = []
    for room in get_last_round_games_and_results(tournament):
        if request.method == 'POST':
            form = ResultGameForm(request.POST, instance=room['result'], prefix=room['game'].id)
            all_is_valid &= form.is_valid()
            if form.is_valid():
                form.save()
        else:
            form = ResultGameForm(instance=room['result'], prefix=room['game'].id)
            form.initial['game'] = room['game'].id
        # else:
        #     form = ResultGameForm(instance=room['result'], prefix=room['game'].id)

        forms.append({
            'game': room['game'],
            'result': form,
        })

    if all_is_valid and request.method == 'POST':
        return redirect('tournament:play', tournament_id=tournament_id)

    return render(
        request,
        'tournament/result_round.html',
        {
            'tournament': tournament,
            'forms': forms,
        }
    )


@login_required(login_url=reverse_lazy('account_login'))
def remove_round(request, tournament_id):
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    remove_last_round(tournament)
    return redirect('tournament:play', tournament_id=tournament_id)


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
        'tournament/team_list.html',
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

    is_check_page = request.path == reverse('tournament:check_team_list', args=[tournament_id])
    member_count = tournament.teamtournamentrel_set.filter(role=ROLE_MEMBER).count()
    if is_check_page and request.method == 'POST' and not member_count % TEAM_IN_GAME:
        return redirect('tournament:check_adjudicator_list', tournament_id=tournament_id)

    return render(
        request,
        'tournament/edit_team_list.html',
        {
            'is_check_page': is_check_page,
            'member_count': member_count,
            'forms': forms,
            'id': tournament_id,
        }
    )


def edit_adjudicator_list(request, tournament_id):
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    forms = []
    # TODO Добавить фильтр
    for user_rel in tournament.usertournamentrel_set.all().order_by('user_id'):
        if request.method == 'POST':
            adjudicator = UserRoleForm(request.POST, instance=user_rel, prefix=user_rel.user.id)
            if adjudicator.is_valid():
                adjudicator.save()

        adjudicator = user_rel.user
        form = UserRoleForm(instance=user_rel, prefix=adjudicator.id)
        forms.append({
            'adjudicator': adjudicator,
            'adjudicator_form': form
        })

    is_check_page = request.path == reverse('tournament:check_adjudicator_list', args=[tournament_id])
    member_count = tournament.teamtournamentrel_set.filter(role=ROLE_MEMBER).count()
    chair_count = tournament.usertournamentrel_set.filter(role=ROLE_CHAIR).count()
    if is_check_page and request.method == 'POST' and chair_count >= member_count // TEAM_IN_GAME:
        return redirect('tournament:play', tournament_id=tournament_id)

    return render(
        request,
        'tournament/edit_adjudicator_list.html',
        {
            'is_check_page': is_check_page,
            'chair_count': chair_count,
            'chair_need': member_count // TEAM_IN_GAME,
            'forms': forms,
            'id': tournament_id,
        }
    )


def show_adjudicator_list(request, tournament_id):
    tournament = get_object_or_404(Tournament, pk=tournament_id)

    return render(
        request,
        'tournament/adjudicator_list.html',
        {
            'adjudicators': tournament.usertournamentrel_set.filter(
                role_id__in=[
                    ROLE_ADJUDICATOR_REGISTERED[0],  # TODO Разобраться, почему тут приходит картеж
                    ROLE_OWNER,
                    ROLE_TEAM_REGISTERED,
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
