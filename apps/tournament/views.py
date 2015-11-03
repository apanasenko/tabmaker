import random
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import \
    csrf_protect, \
    ensure_csrf_cookie
from django.core.urlresolvers import \
    reverse_lazy, \
    reverse
from django.shortcuts import \
    render, \
    get_object_or_404, \
    redirect

from apps.profile.utils import json_response
from apps.team.forms import \
    TeamRegistrationForm, \
    TeamWithSpeakerRegistrationForm
from apps.motion.forms import MotionForm
from apps.game.forms import \
    GameForm, \
    ResultGameForm

from .forms import \
    TournamentForm, \
    CheckboxForm, \
    СonfirmForm, \
    RoundForm

from .consts import *
from .messages import *

from .models import \
    AccessToPage, \
    Tournament, \
    TeamTournamentRel, \
    UserTournamentRel

from .logic import \
    can_change_team_role, \
    check_last_round_results, \
    check_teams_and_adjudicators, \
    generate_next_round, \
    generate_playoff, \
    get_games_and_results, \
    get_motions, \
    get_rooms_from_last_round, \
    get_rooms_by_chair_from_last_round, \
    get_tab, \
    get_teams_by_user, \
    publish_last_round, \
    remove_last_round, \
    remove_playoff, \
    user_can_edit_tournament


def access_by_status(name_page=None):
    def decorator_maker(func):

        def check_access_to_page(request, tournament_id, *args, **kwargs):
            tournament = get_object_or_404(Tournament, pk=tournament_id)
            if name_page:
                security = AccessToPage.objects.get(status=tournament.status, page__name=name_page)
                if not security.page.is_public and not user_can_edit_tournament(tournament, request.user):
                    return _show_message(request, """
                        У Вас нет прав для просмотра данной страницы, обратитесь к создателю турнира
                    """)

                if not security.access:
                    return _show_message(request, security.message)

            return func(request, tournament, *args, **kwargs)

        return check_access_to_page

    return decorator_maker


def check_tournament(func):
    def decorator(request, tournament):
        error = check_last_round_results(tournament)
        if error:
            return _show_message(request, error)

        error = check_teams_and_adjudicators(tournament)
        if error:
            return _show_message(request, error)

        return func(request, tournament)

    return decorator


def _confirm_page(request, tournament, need_message, template_body, redirect_to, callback, redirect_args=None):
    if not redirect_args:
        redirect_args = {}
    confirm_form = СonfirmForm(request.POST)
    is_error = False
    if request.method == 'POST' and confirm_form.is_valid():
        message = confirm_form.cleaned_data.get('message', '')
        is_error = not (message == need_message)
        if not is_error:
            callback(tournament)

            return redirect(redirect_to, **redirect_args)

    return render(
        request,
        'tournament/confirm.html',
        {
            'tournament': tournament,
            'form': confirm_form,
            'need_message': need_message,
            'is_error': is_error,
            'template_body': template_body,
            'path': request.path
        }
    )


def _show_message(request, message):
    return render(
        request,
        'main/message.html',
        {
            'message': message,
        }
    )


def _convert_tab_to_table(table: list, show_all):

    def _playoff_position(res):
        if res.playoff_position > res.count_playoff_rounds:
            return 'Победители'
        elif res.playoff_position == res.count_playoff_rounds:
            return 'Финалисты'
        elif res.playoff_position == 0:
            return '-'
        else:
            return '1/' + str(2 ** (res.count_playoff_rounds - res.playoff_position))

    lines = []
    count_rounds = max(list(map(lambda x: len(x.rounds), table)) + [0])
    line = ['№', 'Команда', 'Сумма баллов', 'Плейофф', 'Сумма спикерских']

    for i in range(1, count_rounds + 1):
        line.append('Раунд %s' % i)
    lines.append(line)

    for team in table:
        team.show_all = show_all

    table = sorted(table, reverse=True)
    for i in range(len(table)):
        line = []
        n = lines[-1][0] if i > 0 and table[i - 1] == table[i] else i + 1
        line += [n, table[i].team.name, table[i].sum_points, _playoff_position(table[i]), table[i].sum_speakers]
        for cur_round in table[i].rounds:
            round_res = str(cur_round.points * (not cur_round.is_closed or show_all))
            if show_all:
                round_res += " / %s+%s" % (cur_round.speaker_1, cur_round.speaker_2)
            line.append(round_res)
        lines.append(line)

    return lines


def _convert_tab_to_speaker_table(table: list, is_show):
    speakers = []
    for team_result in table:
        speakers += team_result.extract_speakers_result()

    if is_show:
        speakers = sorted(speakers, reverse=True)
    else:
        random.shuffle(speakers)

    lines = []
    count_rounds = max(list(map(lambda x: len(x.points), speakers)) + [0])
    head = ['№', 'Спикер', 'Команда', 'Сумма баллов']

    for i in range(1, count_rounds + 1):
        head.append('Раунд %s' % i)
    lines.append(head)

    for i in range(len(speakers)):
        line = []
        n = lines[-1][0] if i > 0 and speakers[i - 1] == speakers[i] else i + 1
        line += [n, speakers[i].user.name(), speakers[i].team.name, speakers[i].sum_points() * int(is_show)]
        for point in speakers[i].points:
            line.append(point * int(is_show))
        lines.append(line)

    return lines


def _get_or_check_round_result_forms(request, rooms):
    all_is_valid = True
    forms = []
    for room in get_games_and_results(rooms):
        if request.method == 'POST':
            form = ResultGameForm(request.POST, instance=room['result'], prefix=room['game'].id)
            all_is_valid &= form.is_valid()
            if form.is_valid():
                form.save()
        else:
            form = ResultGameForm(instance=room['result'], prefix=room['game'].id)
            form.initial['game'] = room['game'].id

        forms.append({
            'game': room['game'],
            'result': form,
        })
    return all_is_valid, forms


##################################
#    Management of tournament    #
##################################

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

            return redirect('tournament:show', tournament_id=tournament_obj.id)

    else:
        tournament_form = TournamentForm()

    return render(
        request,
        'tournament/new.html',
        {
            'form': tournament_form,
        }
    )


@access_by_status(name_page='show')
def show(request, tournament):
    is_chair = request.user.is_authenticated() \
        and tournament.status in [STATUS_PLAYOFF, STATUS_STARTED] \
        and get_rooms_by_chair_from_last_round(tournament, request.user)
    return render(
        request,
        'tournament/show.html',
        {
            'tournament': tournament,
            'team_tournament_rels': tournament.teamtournamentrel_set.all().order_by('-role_id', '-id'),
            'adjudicators': tournament.usertournamentrel_set.filter(role__in=ADJUDICATOR_ROLES).order_by('user_id'),
            'is_owner': user_can_edit_tournament(tournament, request.user),
            'is_chair': is_chair
        }
    )


@login_required(login_url=reverse_lazy('account_login'))
@access_by_status(name_page='edit')
def edit(request, tournament):
    if request.method == 'POST':
        tournament_form = TournamentForm(request.POST, instance=tournament)
        if tournament_form.is_valid():
            tournament_form.save()

            return _show_message(request, 'Турнир изменён')

    else:
        tournament_form = TournamentForm(instance=tournament)

    return render(
        request,
        'tournament/edit.html',
        {
            'form': tournament_form,
            'tournament': tournament,
            'team_tournament_rels': tournament.teamtournamentrel_set.all().order_by('-role_id', '-id'),
            'adjudicators': tournament.usertournamentrel_set.filter(role__in=ADJUDICATOR_ROLES).order_by('user_id'),
        }
    )


@login_required(login_url=reverse_lazy('account_login'))
@access_by_status(name_page='play')
def play(request, tournament):
    return render(
        request,
        'tournament/play.html',
        {
            'tournament': tournament,
        }
    )


@access_by_status(name_page='result')
def result(request, tournament):
    is_owner = user_can_edit_tournament(tournament, request.user)
    show_all = tournament.status == STATUS_FINISHED or is_owner

    return render(
        request,
        'tournament/result.html',
        {
            'tournament': tournament,
            'team_tab': _convert_tab_to_table(get_tab(tournament), show_all),
            'speaker_tab': _convert_tab_to_speaker_table(get_tab(tournament), show_all),
            'motions': get_motions(tournament),
            'is_owner': is_owner,
        }
    )


@login_required(login_url=reverse_lazy('account_login'))
@access_by_status(name_page='remove')
def remove(request, tournament):
    need_message = 'Удалить'
    redirect_to = 'main:index'
    template_body = 'tournament/remove_message.html'

    def tournament_delete(tournament_):
        tournament_.delete()

    return _confirm_page(request, tournament, need_message, template_body, redirect_to, tournament_delete)


@login_required(login_url=reverse_lazy('account_login'))
@access_by_status(name_page='edit')  # TODO Добавить в таблицу
def print_users(request, tournament):
    return render(
        request,
        'tournament/users_list_for_print.html',
        {
            'teams': tournament.team_members.all()
        }
    )


##################################
#   Change status of tournament  #
##################################

@login_required(login_url=reverse_lazy('account_login'))
@access_by_status(name_page='registration opening')
def registration_opening(request, tournament):
    tournament.set_status(STATUS_REGISTRATION)
    return redirect('tournament:show', tournament_id=tournament.id)


@login_required(login_url=reverse_lazy('account_login'))
@access_by_status(name_page='registration closing')
def registration_closing(request, tournament):
    if tournament.status == STATUS_STARTED and tournament.cur_round > 0:
        return _show_message(request, MSG_MUST_REMOVE_ROUNDS)

    tournament.set_status(STATUS_PREPARATION)
    return redirect('tournament:show', tournament_id=tournament.id)


@login_required(login_url=reverse_lazy('account_login'))
@access_by_status(name_page='start')
def start(request, tournament):
    if tournament.status == STATUS_PREPARATION:
        error_message = check_teams_and_adjudicators(tournament)
    else:
        error_message = '' if remove_playoff(tournament) else MSG_MUST_REMOVE_PLAYOFF_ROUNDS

    if error_message:
        return _show_message(request, error_message)

    tournament.set_status(STATUS_STARTED)
    return redirect('tournament:play', tournament_id=tournament.id)


@login_required(login_url=reverse_lazy('account_login'))
@access_by_status(name_page='break')
def generate_break(request, tournament):
    tab = sorted(get_tab(tournament), reverse=True)
    table = _convert_tab_to_table(tab, True)
    teams_in_break = []
    teams = []
    for i in range(len(tab)):
        if request.method == 'POST':
            form = CheckboxForm(request.POST, prefix=i)
            if form.is_valid() and form.cleaned_data.get('is_check', False):
                teams_in_break.append(tab[i].team)
        else:
            form = CheckboxForm(
                initial={
                    'id': tab[i].team.id,
                    'is_check': i < tournament.count_teams_in_break
                },
                prefix=i
            )
        teams.append({
            'checkbox': form,
            'result': table[i + 1],
        })

    error_message = ''
    if request.method == 'POST':
        if len(teams_in_break) != tournament.count_teams_in_break:
            error_message = 'Вы должны выбрать %s команд(ы), которые делают брейк' % tournament.count_teams_in_break
        else:
            generate_playoff(tournament, teams_in_break)
            tournament.set_status(STATUS_PLAYOFF)

            return redirect('tournament:play', tournament_id=tournament.id)

    return render(
        request,
        'tournament/break.html',
        {
            'error': error_message,
            'tournament': tournament,
            'header': table[0],
            'teams': teams,
        }
    )


@login_required(login_url=reverse_lazy('account_login'))
@access_by_status(name_page='finished')
def finished(request, tournament):
    need_message = 'Завершить'
    redirect_to = 'tournament:show'
    template_body = 'tournament/finished_message.html'
    redirect_args = {'tournament_id': tournament.id}

    def tournament_finished(tournament_):
        tournament_.set_status(STATUS_FINISHED)

    return _confirm_page(request, tournament, need_message, template_body, redirect_to, tournament_finished,
                         redirect_args)


##################################
#      Management of rounds      #
##################################

@login_required(login_url=reverse_lazy('account_login'))
@access_by_status(name_page='round_next')
@check_tournament
def next_round(request, tournament):
    if request.method == 'POST':
        motion_form = MotionForm(request.POST)
        round_form = RoundForm(request.POST)
        if motion_form.is_valid() and round_form.is_valid():
            round_obj = round_form.save(commit=False)
            round_obj.motion = motion_form.save()
            error = generate_next_round(tournament, round_obj)
            if error:
                _show_message(request, error)

            return redirect('tournament:edit_round', tournament_id=tournament.id)
    else:
        motion_form = MotionForm()
        round_form = RoundForm()

    return render(
        request,
        'tournament/next_round.html',
        {
            'tournament': tournament,
            'motion_form': motion_form,
            'round_form': round_form,
        }
    )


@access_by_status(name_page='round_show')
def show_round(request, tournament):
    rooms = get_rooms_from_last_round(tournament, True)
    if not rooms or not rooms[0].round.is_public:
        return _show_message(request, MSG_ROUND_NOT_PUBLIC)

    return render(
        request,
        'tournament/show_round.html',
        {
            'rooms': rooms,
            'round': None if not rooms else rooms[0].round
        },
    )


@login_required(login_url=reverse_lazy('account_login'))
@access_by_status(name_page='round_next')  # TODO Добавить в таблицу доступа
def presentation_round(request, tournament):
    rooms = get_rooms_from_last_round(tournament, True)
    return render(
        request,
        'tournament/presentation_round.html',
        {
            'rooms': rooms,
            'round': None if not rooms else rooms[0].round
        },
    )


@login_required(login_url=reverse_lazy('account_login'))
@access_by_status(name_page='round_edit')
def publish_round(request, tournament):
    if not publish_last_round(tournament):
        _show_message(request, MSG_ROUND_NOT_EXIST)

    return redirect('tournament:play', tournament_id=tournament.id)


@login_required(login_url=reverse_lazy('account_login'))
@access_by_status(name_page='round_edit')
def edit_round(request, tournament):
    forms = []
    all_is_valid = True
    for room in get_rooms_from_last_round(tournament):
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
        return redirect('tournament:play', tournament_id=tournament.id)

    return render(
        request,
        'tournament/edit_round.html',
        {
            'tournament': tournament,
            'forms': forms,
        }
    )


@login_required(login_url=reverse_lazy('account_login'))
@access_by_status(name_page='round_result')
def result_round(request, tournament):
    is_owner = user_can_edit_tournament(tournament, request.user)
    if is_owner:
        rooms = get_rooms_from_last_round(tournament)
    else:
        rooms = get_rooms_by_chair_from_last_round(tournament, request.user)

    if not is_owner and not rooms:
        return _show_message(request, MSG_NO_ACCESS_IN_RESULT_PAGE)

    is_valid, forms = _get_or_check_round_result_forms(request, rooms)

    if is_valid and request.method == 'POST':
        if is_owner:
            return redirect('tournament:play', tournament_id=tournament.id)
        else:
            return redirect('tournament:show', tournament_id=tournament.id)

    return render(
        request,
        'tournament/result_round.html',
        {
            'tournament': tournament,
            'forms': forms,
        }
    )


@login_required(login_url=reverse_lazy('account_login'))
@access_by_status(name_page='round_remove')
def remove_round(request, tournament):
    if remove_last_round(tournament):
        return redirect('tournament:play', tournament_id=tournament.id)
    elif tournament.status == STATUS_PLAYOFF:
        return _show_message(request, 'Нет сыграных раундов плейофф. Для удаления отборочных раундов отмените брейк')
    else:
        return _show_message(request, 'Нет сыграных раундов.')


##################################
#      Management of teams       #
##################################

@login_required(login_url=reverse_lazy('account_login'))
@access_by_status(name_page='team/adju. registration')
def registration_team(request, tournament):
    if request.method == 'POST':
        team_form = TeamWithSpeakerRegistrationForm(request.POST)
        if team_form.is_valid():
            team = team_form.save(speaker_1=request.user)
            TeamTournamentRel.objects.create(
                team=team,
                tournament=tournament,
                role=ROLE_TEAM_REGISTERED
            )
            return _show_message(request, 'Вы успешно зарегистрировались на %s' % tournament.name)

    else:
        team_form = TeamWithSpeakerRegistrationForm(initial={'speaker_1': request.user.email})

    return render(
        request,
        'tournament/registration.html',
        {
            'form': team_form,
            'tournament': tournament,
            'show_speaker_1': False,
        }
    )


@login_required(login_url=reverse_lazy('account_login'))
@access_by_status(name_page='team/adju. add')
def add_team(request, tournament):
    saved_team = None
    if request.method == 'POST':
        team_form = TeamRegistrationForm(request.POST)
        if team_form.is_valid():
            team = team_form.save()
            TeamTournamentRel.objects.create(
                team=team,
                tournament=tournament,
                role=ROLE_TEAM_REGISTERED
            )
            saved_team = team.name
            team_form = TeamRegistrationForm()
    else:
        team_form = TeamRegistrationForm()

    return render(
        request,
        'tournament/registration.html',
        {
            'form': team_form,
            'tournament': tournament,
            'show_speaker_1': True,
            'saved_team': saved_team,
        }
    )


@ensure_csrf_cookie
@login_required(login_url=reverse_lazy('account_login'))
@access_by_status(name_page='team/adju. edit')
def edit_team_list(request, tournament):
    return render(
        request,
        'tournament/edit_team_list.html',
        {
            'is_check_page': request.path == reverse('tournament:check_team_list', args=[tournament.id]),
            'tournament': tournament,
            'team_tournament_rels': tournament.teamtournamentrel_set.all().order_by('-role_id', '-id'),
            'statuses': TEAM_ROLES,
            'can_remove_teams': tournament.cur_round == 0,
            'member_role': ROLE_MEMBER,
        }
    )


@csrf_protect
@login_required(login_url=reverse_lazy('account_login'))
@access_by_status(name_page='team/adju. edit')
def team_role_update(request, tournament):
    if request.method != 'POST' or not request.is_ajax():
        return HttpResponseBadRequest

    rel = get_object_or_404(TeamTournamentRel, pk=request.POST.get('rel_id', '0'))
    new_role = get_object_or_404(TournamentRole, pk=request.POST.get('new_role_id', '0'))
    if new_role not in TEAM_ROLES:
        return json_response('bad', 'Недопустимая роль команды')

    can_change, message = can_change_team_role(rel, new_role)
    if not can_change:
        return json_response('bad', message)

    rel.role = new_role
    rel.save()

    return json_response('ok', 'Статус команды успешно изменён')


##################################
#   Management of adjudicator    #
##################################

@login_required(login_url=reverse_lazy('account_login'))
@access_by_status(name_page='team/adju. registration')
def registration_adjudicator(request, tournament):
    create = UserTournamentRel.objects.get_or_create(
        user=request.user,
        tournament=tournament,
        role=ROLE_ADJUDICATOR_REGISTERED[0]
    )
    message = 'Вы успешно зарегистрировались на %s как судья' % tournament.name if create[1] \
        else 'Вы уже зарегистрировались на %s как судья' % tournament.name

    return _show_message(request, message)


@login_required(login_url=reverse_lazy('account_login'))
@access_by_status(name_page='team/adju. add')
def add_adjudicator(request, tournament):
    # TODO Добавление судьи
    return redirect('tournament:edit_adjudicator_list', tournament_id=tournament.id)


@login_required(login_url=reverse_lazy('account_login'))
@access_by_status(name_page='team/adju. edit')
def edit_adjudicator_list(request, tournament):
    return render(
        request,
        'tournament/edit_adjudicator_list.html',
        {
            'is_check_page': request.path == reverse('tournament:check_adjudicator_list', args=[tournament.id]),
            'chair_need': tournament.teamtournamentrel_set.filter(role=ROLE_MEMBER).count() // TEAM_IN_GAME,
            'user_tournament_rels': tournament.usertournamentrel_set.filter(role__in=ADJUDICATOR_ROLES).order_by(
                'user_id'),
            'statuses': ADJUDICATOR_ROLES,
            'chair_role': ROLE_CHAIR,
            'tournament': tournament,
        }
    )


@csrf_protect
@login_required(login_url=reverse_lazy('account_login'))
@access_by_status(name_page='team/adju. edit')
def adjudicator_role_update(request, tournament):
    if request.method != 'POST' or not request.is_ajax():
        return HttpResponseBadRequest

    rel = get_object_or_404(UserTournamentRel, pk=request.POST.get('rel_id', '0'))
    new_role = get_object_or_404(TournamentRole, pk=request.POST.get('new_role_id', '0'))
    if new_role not in ADJUDICATOR_ROLES:
        return json_response('bad', 'Недопустимая роль судьи')

    teams = get_teams_by_user(rel.user, rel.tournament)
    if new_role in [ROLE_CHAIR, ROLE_CHIEF_ADJUDICATOR, ROLE_WING] and teams:
        return json_response(
            'bad', '%s из команды "%s" является участником турнира' % (rel.user.name(), teams[0].team.name)
        )

    rel.role = new_role
    rel.save()

    return json_response('ok', 'Статус судьи успешно изменён')
