import random
import logging

from datetime import date, timedelta

# from django.db.models import Count, Q
# from django.shortcuts import render

# from apps.tournament.consts import *
# from apps.tournament.models import Tournament
# from apps.tournament.utils import paging

from django.contrib.auth.decorators import login_required
from django.db.models import Case, When, IntegerField
from django.urls import \
    reverse_lazy, \
    reverse
from django.http import \
    HttpResponseBadRequest, \
    Http404

from django.shortcuts import \
    render, \
    get_object_or_404, \
    redirect
from django.views.decorators.csrf import \
    csrf_protect, \
    ensure_csrf_cookie

from .forms import EditForm

from .utils import \
    json_response, \
    paging

from .consts import *
from .forms import \
    TournamentForm, \
    CheckboxForm, \
    СonfirmForm, \
    RoundForm, \
    ActivateResultForm, \
    GameForm, \
    MotionForm
from .logic import \
    can_change_team_role, \
    check_games_results_exists, \
    check_final, \
    check_last_round_results, \
    check_teams_and_adjudicators, \
    generate_next_round, \
    generate_playoff, \
    get_all_rounds_and_rooms, \
    get_games_and_results, \
    get_rooms_by_user, \
    get_motions, \
    get_rooms_from_last_round, \
    get_tab, \
    get_teams_by_user, \
    publish_last_round, \
    remove_last_round, \
    remove_playoff, \
    user_can_edit_tournament
from .messages import *
from .models import \
    AccessToPage, \
    Tournament, \
    TeamTournamentRel, \
    TelegramToken, \
    UserTournamentRel, \
    User

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Q


def access_by_status(name_page=None, only_owner=False):
    # TODO Страницы в константы
    # TODO Закешировать массив с уровнем доступа
    def decorator_maker(func):

        def check_access_to_page(request, tournament_id, *args, **kwargs):
            tournament = get_object_or_404(Tournament, pk=tournament_id)
            if name_page:
                security = AccessToPage.objects.filter(status=tournament.status, page__name=name_page) \
                    .select_related('page').first()
                if not security.page.is_public and not user_can_edit_tournament(tournament, request.user, only_owner):
                    return _show_message(request, MSG_ERROR_TO_ACCESS)

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

        error = check_final(tournament)
        if error:
            return _show_message(request, error)

        return func(request, tournament)

    return decorator


def ajax_request(func):
    def decorator(request, *args, **kwargs):
        if request.method != 'POST' or not request.is_ajax():
            return HttpResponseBadRequest

        return func(request, *args, **kwargs)

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
        if not res.count_playoff_rounds:
            return LBL_NOT_IN_BREAK
        if res.playoff_position > res.count_playoff_rounds:
            return LBL_WINNER
        elif res.playoff_position == res.count_playoff_rounds:
            return LBL_FINALISTS
        elif res.playoff_position == 0:
            return LBL_NOT_IN_BREAK
        else:
            return LBL_ONE_p % str(2 ** (res.count_playoff_rounds - res.playoff_position))

    lines = []
    count_rounds = max(list(map(lambda x: len(x.rounds), table)) + [0])
    line = [LBL_N, LBL_TEAM, LBL_SUM_POINTS, LBL_PLAYOFF, LBL_SUM_SPEAKERS]

    for i in range(1, count_rounds + 1):
        line.append(LBL_ROUND_p % i)
    lines.append(line)

    for team in table:
        team.show_all = show_all

    table = sorted(table, reverse=True)
    for i in range(len(table)):
        line = []
        n = lines[-1][0] if i > 0 and table[i - 1] == table[i] else i + 1
        line += [n, table[i].team.name, table[i].sum_points, _playoff_position(table[i]), table[i].sum_speakers]
        for cur_round in table[i].rounds:
            round_res = str(cur_round.points * bool(not cur_round.is_closed or show_all))
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
    head = [LBL_N, LBL_SPEAKER, LBL_TEAM, LBL_SUM_SPEAKERS]

    for i in range(1, count_rounds + 1):
        head.append(LBL_ROUND_p % i)
    lines.append(head)

    for i in range(len(speakers)):
        line = []
        n = lines[-1][0] if i > 0 and speakers[i - 1] == speakers[i] else i + 1
        line += [n, speakers[i].user.name(), speakers[i].team.name, speakers[i].sum_points() * int(is_show)]
        for point in speakers[i].points:
            line.append(point * int(is_show))
        lines.append(line)

    return lines


def _get_or_check_round_result_forms(request, rooms, is_admin=False, is_playoff=False, is_final=False):
    from .forms import \
        FinalGameResultForm, \
        PlayoffGameResultForm, \
        QualificationGameResultForm

    all_is_valid = True
    forms = []

    ResultForm = FinalGameResultForm if is_final \
        else PlayoffGameResultForm if is_playoff \
        else QualificationGameResultForm

    for room in get_games_and_results(rooms):
        activate_form = ActivateResultForm(request.POST or None, prefix='af_%s' % room['game'].id)

        if request.method == 'POST' and activate_form.is_valid() and activate_form.is_active():
            result_form = ResultForm(request.POST, instance=room['result'], prefix='rf_%s' % room['game'].id)
            all_is_valid &= result_form.is_valid()
            if result_form.is_valid():
                result_form.save()
        else:
            result_form = ResultForm(instance=room['result'], prefix='rf_%s' % room['game'].id)
            activate_form.init(is_admin)
            result_form.initial['game'] = room['game'].id

        forms.append({
            'game': room['game'],
            'result': result_form,
            'activate_result': activate_form,
            'show_checkbox': is_admin,
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

            CustomForm.get_or_create(tournament_obj, FORM_REGISTRATION_TYPE)
            CustomForm.get_or_create(tournament_obj, FORM_ADJUDICATOR_TYPE)

            return redirect('tournament:created', tournament_id=tournament_obj.id)

    else:
        tournament_form = TournamentForm()

    return render(
        request,
        'tournament/new.html',
        {
            'form': tournament_form,
        }
    )


@login_required(login_url=reverse_lazy('account_login'))
@access_by_status(name_page='edit')
def created(request, tournament):
    return render(
        request,
        'tournament/created.html',
        {
            'tournament': tournament,
        }
    )


@access_by_status(name_page='show')
def show(request, tournament):

    if request.GET.get('new', None):
        return show2(request, tournament)

    is_chair = request.user.is_authenticated \
        and tournament.status in [STATUS_PLAYOFF, STATUS_STARTED] \
        and get_rooms_from_last_round(tournament, False, request.user).count()

    need_show_feedback_button = request.user.is_authenticated \
        and get_rooms_by_user(tournament, request.user) \
        and CustomForm.objects.filter(tournament=tournament, form_type=FORM_FEEDBACK_TYPE).count()

    return render(
        request,
        'tournament/show.html',
        {
            'tournament': tournament,
            'team_tournament_rels': tournament.get_teams(),
            'adjudicators': tournament.get_users(ADJUDICATOR_ROLES),
            'is_owner': user_can_edit_tournament(tournament, request.user),
            'is_chair': is_chair,
            'need_show_feedback_button': need_show_feedback_button,
        }
    )


# @access_by_status(name_page='show')
def show2(request, tournament):

    # is_chair = request.user.is_authenticated \
    #     and tournament.status in [STATUS_PLAYOFF, STATUS_STARTED] \
    #     and get_rooms_from_last_round(tournament, False, request.user).count()
    #
    # need_show_feedback_button = request.user.is_authenticated \
    #     and get_rooms_by_user(tournament, request.user) \
    #     and CustomForm.objects.filter(tournament=tournament, form_type=FORM_FEEDBACK_TYPE).count()

    is_owner = user_can_edit_tournament(tournament, request.user)

    tabs = []

    # Текущий раунд
    if tournament.status in [STATUS_STARTED, STATUS_PLAYOFF]:
        tab_config = {'title': 'Раунд'}
        rooms = get_rooms_from_last_round(tournament, True)
        if not rooms or not rooms[0].round.is_public:
            tab_config['message'] = MSG_ROUND_NOT_PUBLIC
        else:
            tab_config['data'] = rooms
            tab_config['template'] = 'tournament/tabs/public/round.html'

        tabs.append(tab_config)

    # Командный теб + Спикерский теб
    if tournament.status in [STATUS_STARTED, STATUS_PLAYOFF, STATUS_FINISHED]:
        show_all = tournament.status == STATUS_FINISHED or is_owner
        results = get_tab(tournament)

        tab_config = {'title': 'Результаты команд'}
        if not results:
            tab_config['message'] = 'Результатов нет'
        else:
            tab_config['data'] = _convert_tab_to_table(results, show_all)
            tab_config['template'] = 'tournament/tabs/public/tab.html'

        tabs.append(tab_config)

        if tournament.status == STATUS_FINISHED:
            tab_config = {'title': 'Результаты спикеров'}
            if not results:
                tab_config['message'] = 'Результатов нет'
            else:
                tab_config['data'] = _convert_tab_to_speaker_table(results, show_all)
                tab_config['template'] = 'tournament/tabs/public/tab.html'

            tabs.append(tab_config)

        tabs.append({
            'title': 'Темы',
            'data': get_motions(tournament),
            'template': 'tournament/tabs/public/motions.html',
        })

        if tournament.status == STATUS_FINISHED:
            tabs.append({
                'title': 'Раунды',
                'data': get_all_rounds_and_rooms(tournament),
                'template': 'tournament/tabs/public/results.html',
            })

    tabs.append({
        'title': 'О турнире',
        'data': tournament,
        'template': 'tournament/tabs/public/info.html',
    })

    tab_config = {'title': 'Команды'}
    if not is_owner and tournament.status == STATUS_REGISTRATION and tournament.is_registration_hidden:
        tab_config['message'] = 'Информация закрыта'
        tab_config['comment'] = 'Организаторы турнира скрыли инфомацию о уже зарегистрированных командах'
    else:
        teams = tournament.get_teams()
        if not len(teams):
            tab_config['message'] = 'Пока никто не зарегистрировался'
            tab_config['comment'] = 'Вы можете стать первым участником'
        else:
            tab_config['data'] = teams
            tab_config['template'] = 'tournament/tabs/public/teams.html'

    tabs.append(tab_config)

    tab_config = {'title': 'Судьи'}
    adjudicators = tournament.get_users(ADJUDICATOR_ROLES)
    if not len(adjudicators):
        tab_config['message'] = 'Пока никто не зарегистрировался'
        tab_config['comment'] = 'Вы можете стать первым cудьей'
    else:
        tab_config['data'] = adjudicators
        tab_config['template'] = 'tournament/tabs/public/adjudicators.html'

    tabs.append(tab_config)

    tabs.append({
        'title': 'На карте',
        'data': True,
        'template': 'tournament/tabs/public/map.html',
    })

    return render(
        request,
        'tournament/show2.html',
        {
            'tournament': tournament,
            'is_owner': is_owner,
            'tabs': tabs,
            # 'is_chair': is_chair,
            # 'need_show_feedback_button': need_show_feedback_button,
            # 'user_messages': messages.get_messages(request),
        }
    )


@login_required(login_url=reverse_lazy('account_login'))
@access_by_status(name_page='edit')
def edit(request, tournament):
    if request.method == 'POST':
        tournament_form = TournamentForm(request.POST, instance=tournament)
        if tournament_form.is_valid():
            tournament_form.save()

            return _show_message(request, MSG_TOURNAMENT_CHANGED)

    else:
        tournament_form = TournamentForm(instance=tournament)

    team_form = CustomForm.get_or_create(tournament, FORM_REGISTRATION_TYPE)
    team_questions = CustomQuestion.objects.filter(form=team_form).select_related('alias').order_by('position')

    adjudicator_form = CustomForm.get_or_create(tournament, FORM_ADJUDICATOR_TYPE)
    adjudicator_questions = CustomQuestion.objects.filter(form=adjudicator_form) \
        .select_related('alias') \
        .order_by('position')

    return render(
        request,
        'tournament/edit.html',
        {
            'form': tournament_form,
            'tournament': tournament,
            'team_form': team_form,
            'team_questions': team_questions,
            'adjudicator_form': adjudicator_form,
            'adjudicator_questions': adjudicator_questions,
            'required_aliases': REQUIRED_ALIASES,
            'actions': CUSTOM_FORM_AJAX_ACTIONS,
        }
    )


@access_by_status(name_page='result')
def result(request, tournament):
    is_owner = user_can_edit_tournament(tournament, request.user)
    show_all = tournament.status == STATUS_FINISHED or is_owner
    tab = get_tab(tournament)

    return render(
        request,
        'tournament/result.html',
        {
            'tournament': tournament,
            'team_tab': _convert_tab_to_table(tab, show_all),
            'speaker_tab': _convert_tab_to_speaker_table(tab, show_all),
            'motions': get_motions(tournament),
            'is_owner': is_owner,
        }
    )


@access_by_status(name_page='result_all')
def result_all_rounds(request, tournament):
    is_owner = user_can_edit_tournament(tournament, request.user)
    if not is_owner and tournament.status != STATUS_FINISHED:
        return _show_message(request, MSG_RESULT_NOT_PUBLISHED)

    return render(
        request,
        'tournament/round_results_show.html',
        {
            'tournament': tournament,
            'results': get_all_rounds_and_rooms(tournament),
            'is_owner': is_owner,
        }
    )


@login_required(login_url=reverse_lazy('account_login'))
@access_by_status(name_page='remove')
def remove(request, tournament):
    if tournament.id == 1:
        return _show_message(request, 'Нельзя удалить тестовый турнир')
    need_message = CONFIRM_MSG_REMOVE
    redirect_to = 'main:index'
    template_body = 'tournament/remove_message.html'

    def tournament_delete(tournament_):
        tournament_.delete()

    return _confirm_page(request, tournament, need_message, template_body, redirect_to, tournament_delete)


@login_required(login_url=reverse_lazy('account_login'))
@access_by_status(name_page='edit')
def print_users(request, tournament):
    return render(
        request,
        'tournament/users_list_for_print.html',
        {
            'teams': tournament.team_members.all()
        }
    )


def feedback(request):
    from django.core.mail import mail_managers

    if request.method == 'POST':
        who = ''
        if request.user.is_authenticated:
            who = '%s (%s)' % (request.user.get_full_name(), request.user.email)

        mail_managers(
            'Tabmaker Feedback',
            '''
            Кто %s \n\n
            Что в Tabmaker сделано хорошо:\n
            %s \n\n\n
            Что в Tabmaker можно улучшить:\n
            %s \n\n\n
            Предложения или пожелания:\n
            %s \n\n\n
            Оценка:\n
            %d \n\n\n
            ''' % (
                who,
                request.POST.get('already_good', ''),
                request.POST.get('can_be_batter', ''),
                request.POST.get('what_you_want', ''),
                int(request.POST.get('nps', 0))
            )
        )

        return _show_message(request, 'Спасибо за ваш отзыв')

    return render(
        request,
        'main/tabmaker_feedback.html'
    )


def support(request):
    from django.core.mail import mail_managers

    if request.method == 'POST':
        who = '%s (%s)' % (request.user.get_full_name(), request.user.email) \
            if request.user.is_authenticated \
            else 'noname'

        mail_managers(
            'Tabmaker: Somebody need help!',
            '''
            Кто %s \n\n
            Проблема:\n
            %s \n\n\n
            Контакты:\n
            %s
            ''' % (
                who,
                request.POST.get('problem', ''),
                request.POST.get('contacts', ''),
            )
        )

        return _show_message(request, 'Мы постараемся ответить как можно быстрее')

    return render(
        request,
        'main/support.html'
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
    return redirect('tournament:show', tournament_id=tournament.id)


@login_required(login_url=reverse_lazy('account_login'))
@access_by_status(name_page='break')
def generate_break(request, tournament):
    tab = sorted(get_tab(tournament), reverse=True)
    table = _convert_tab_to_table(tab, True)
    teams_in_break = []
    teams = []
    for i in range(len(tab)):
        if request.method == 'POST':
            form = CheckboxForm(request.POST, prefix=i, use_required_attribute=False)
            if form.is_valid() and form.cleaned_data.get('is_check', False):
                teams_in_break.append(tab[i].team)
        else:
            form = CheckboxForm(
                initial={
                    'id': tab[i].team.id,
                    'is_check': i < tournament.count_teams_in_break
                },
                prefix=i,
                use_required_attribute=False
            )
        teams.append({
            'checkbox': form,
            'result': table[i + 1],
        })

    error_message = ''
    if request.method == 'POST':
        if len(teams_in_break) != tournament.count_teams_in_break:
            error_message = MSG_SELECT_N_TEAMS_TO_BREAK_p % tournament.count_teams_in_break
        else:
            generate_playoff(tournament, teams_in_break)
            tournament.set_status(STATUS_PLAYOFF)

            return redirect('tournament:show', tournament_id=tournament.id)

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
    need_message = CONFIRM_MSG_FINISHED
    redirect_to = 'main:feedback'
    redirect_args = {}
    template_body = 'tournament/finished_message.html'

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
            'rooms': rooms
        },
    )


@login_required(login_url=reverse_lazy('account_login'))
@access_by_status(name_page='round_next')
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
    try:
        cur_round = publish_last_round(tournament)
    except Exception as exception :
        return _show_message(request, exception)

    try:
        from . telegrambot import TabmakerBot
        from django_telegrambot.apps import DjangoTelegramBot

        rooms = get_rooms_from_last_round(tournament)
        TabmakerBot.send_round_notifications(DjangoTelegramBot.getBot(), cur_round, rooms),
    except Exception as exception :
        logging.error(exception)

    return redirect('tournament:show', tournament_id=tournament.id)


@login_required(login_url=reverse_lazy('account_login'))
@access_by_status(name_page='round_edit')
def edit_round(request, tournament):
    forms = []
    all_is_valid = True
    rooms = list(get_rooms_from_last_round(tournament))
    for room in rooms:
        if request.method == 'POST':
            form = GameForm(request.POST, instance=room.game, prefix=room.game.id)
            all_is_valid &= form.is_valid()
            if form.is_valid():
                form.save()
                room.place_id = form.get_place_id()
                room.save()
        else:
            form = GameForm(instance=room.game, prefix=room.game.id)
            form.init_place(room.place)

        form.game = room.game
        forms.append(form)

    if all_is_valid and request.method == 'POST':
        return redirect('tournament:show', tournament_id=tournament.id)

    team_results = {}
    for team_result in get_tab(tournament):
        team_results[team_result.team.id] = team_result.sum_points()

    return render(
        request,
        'tournament/edit_round.html',
        {
            'tournament': tournament,
            'forms': forms,
            'warning': check_games_results_exists(list(map(lambda x: x.game, rooms))),
            'adjudicators': tournament.get_users([ROLE_CHAIR, ROLE_CHIEF_ADJUDICATOR, ROLE_WING]),
            'places': tournament.place_set.filter(is_active=True),
            'team_results': team_results,
        }
    )


@login_required(login_url=reverse_lazy('account_login'))
@access_by_status(name_page='round_result')
def result_round(request, tournament):
    is_admin = user_can_edit_tournament(tournament, request.user)
    chair = None if is_admin else request.user
    rooms = get_rooms_from_last_round(tournament, False, chair)
    is_playoff = tournament.status == STATUS_PLAYOFF
    is_final = is_playoff and get_rooms_from_last_round(tournament).count() == 1

    if not is_admin and not rooms:
        return _show_message(request, MSG_NO_ACCESS_IN_RESULT_PAGE)

    is_valid, forms = _get_or_check_round_result_forms(request, rooms, is_admin, is_playoff, is_final)

    if is_valid and request.method == 'POST':
        return redirect('tournament:show', tournament_id=tournament.id)

    return render(
        request,
        'tournament/result_round.html',
        {
            'tournament': tournament,
            'forms': forms,
            'is_playoff': is_playoff,
            'is_final': is_final,
            'result_template': 'tournament/playoff_result_team.html' if is_playoff else 'tournament/result_team.html',
        }
    )


@login_required(login_url=reverse_lazy('account_login'))
@access_by_status(name_page='round_remove')
def remove_round(request, tournament):
    if remove_last_round(tournament):
        return redirect('tournament:show', tournament_id=tournament.id)
    elif tournament.status == STATUS_PLAYOFF:
        return _show_message(request, MSG_NO_ROUND_IN_PLAYOFF_FOR_REMOVE)
    else:
        return _show_message(request, MSG_ROUND_NOT_EXIST)


##################################
#      Management of teams       #
##################################

@login_required(login_url=reverse_lazy('account_login'))
@access_by_status(name_page='team/adju. registration')
def registration_team(request, tournament):
    from .registration_forms import \
        CustomTeamRegistrationForm, \
        TeamWithSpeakerRegistrationForm

    custom_form = CustomForm.objects.filter(tournament=tournament, form_type=FORM_REGISTRATION_TYPE).first()
    if custom_form:
        RegistrationForm = CustomTeamRegistrationForm
        questions = CustomQuestion.objects.filter(form=custom_form).select_related('alias').order_by('position')
    else:
        RegistrationForm = TeamWithSpeakerRegistrationForm
        questions = None

    if request.method == 'POST':
        team_form = RegistrationForm(tournament, questions, request.POST)
        if team_form.is_valid():
            team = team_form.save(speaker_1=request.user)
            TeamTournamentRel.objects.create(
                team=team,
                tournament=tournament,
                role=ROLE_TEAM_REGISTERED
            )
            if custom_form:
                custom_form_answers = CustomFormAnswers.objects.create(form=custom_form)
                custom_form_answers.set_answers(team_form.get_answers(questions))
                custom_form_answers.save()

            return _show_message(request, MSG_TEAM_SUCCESS_REGISTERED_pp % (team.name, tournament.name))

    else:
        team_form = RegistrationForm(tournament, questions, initial={'speaker_1': request.user.email})

    return render(
        request,
        'tournament/registration_new.html',
        {
            'title': 'Регистрация команды',
            'submit_title': 'Участвовать',
            'action_url': 'tournament:registration_team',
            'form': team_form,
            'tournament': tournament,
        }
    )


@login_required(login_url=reverse_lazy('account_login'))
@access_by_status(name_page='team/adju. add')
def add_team(request, tournament):
    from apps.tournament.registration_forms import TeamRegistrationForm

    saved_team = None
    if request.method == 'POST':
        team_form = TeamRegistrationForm(tournament, request.POST)
        if team_form.is_valid():
            team = team_form.save()
            TeamTournamentRel.objects.create(
                team=team,
                tournament=tournament,
                role=ROLE_TEAM_REGISTERED
            )
            saved_team = team.name
            team_form = TeamRegistrationForm(tournament)
    else:
        team_form = TeamRegistrationForm(tournament)

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


@login_required(login_url=reverse_lazy('account_login'))
@access_by_status(name_page='team/adju. add')
def import_team(request, tournament):
    from apps.tournament.imports import TeamImportForm, ImportTeam

    message = ''
    results = []
    import_form = TeamImportForm(request.POST or None)
    if request.method == 'POST' and import_form.is_valid():
        imports = ImportTeam(import_form)
        try:
            imports.connect_to_worksheet()
            imports.read_titles()
            is_test = int(request.POST.get('is_test', '0')) == 1
            results = imports.import_teams(tournament, is_test)

        except Exception as ex:
            message = str(ex)

        if results:
            return render(
                request,
                'tournament/import_results.html',
                {
                    'results': results,
                    'tournament': tournament,
                    'statuses': {
                        'add': ImportTeam.STATUS_ADD,
                        'exist': ImportTeam.STATUS_EXIST,
                        'fail': ImportTeam.STATUS_FAIL,
                    },
                }
            )

    return render(
        request,
        'tournament/import_team_form.html',
        {
            'message': message,
            'form': import_form,
            'tournament': tournament,
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
            'team_tournament_rels': tournament.get_teams(),
            'statuses': TEAM_ROLES,
            'can_remove_teams': tournament.cur_round == 0,
            'member_role': ROLE_MEMBER,
        }
    )


@csrf_protect
@ajax_request
@login_required(login_url=reverse_lazy('account_login'))
@access_by_status(name_page='team/adju. edit')
def team_role_update(request, tournament):
    rel = get_object_or_404(TeamTournamentRel, pk=request.POST.get('rel_id', '0'))
    new_role = get_object_or_404(TournamentRole, pk=request.POST.get('new_role_id', '0'))
    if new_role not in TEAM_ROLES:
        return json_response(MSG_JSON_BAD, MSG_BAD_TEAM_ROLE)

    can_change, message = can_change_team_role(rel, new_role)
    if not can_change:
        return json_response(MSG_JSON_BAD, message)

    rel.role = new_role
    rel.save()

    return json_response(MSG_JSON_OK, MSG_TEAM_ROLE_CHANGE)


##################################
#   Management of adjudicator    #
##################################

def _registration_adjudicator(tournament: Tournament, user: User):
    if UserTournamentRel.objects.filter(user=user, tournament=tournament, role__in=ADJUDICATOR_ROLES).exists():
        return False

    UserTournamentRel.objects.create(user=user, tournament=tournament, role=ROLE_ADJUDICATOR_REGISTERED)
    return True


@login_required(login_url=reverse_lazy('account_login'))
@access_by_status(name_page='team/adju. registration')
def registration_adjudicator(request, tournament):
    from .registration_forms import CustomAdjudicatorRegistrationForm

    custom_form = CustomForm.objects.filter(tournament=tournament, form_type=FORM_ADJUDICATOR_TYPE).first()

    if not custom_form:
        message = MSG_ADJUDICATOR_SUCCESS_REGISTERED_p % tournament.name \
            if _registration_adjudicator(tournament, request.user) \
            else MSG_ADJUDICATOR_ALREADY_REGISTERED_p % tournament.name
        return _show_message(request, message)

    questions = CustomQuestion.objects.filter(form=custom_form).select_related('alias').order_by('position')
    if request.method == 'POST':
        adjudicator_form = CustomAdjudicatorRegistrationForm(questions, request.POST)
        if adjudicator_form.is_valid():
            if _registration_adjudicator(tournament, request.user):
                custom_form_answers = CustomFormAnswers.objects.create(form=custom_form)
                custom_form_answers.set_answers(adjudicator_form.get_answers(questions))
                custom_form_answers.save()
                return _show_message(request, MSG_ADJUDICATOR_SUCCESS_REGISTERED_p % tournament.name)
            else:
                return _show_message(request, MSG_ADJUDICATOR_ALREADY_REGISTERED_p % tournament.name)
    else:
        adjudicator_form = CustomAdjudicatorRegistrationForm(questions, initial={'adjudicator': request.user.email})

    return render(
        request,
        'tournament/registration_new.html',
        {
            'title': 'Регистрация судьи',
            'submit_title': 'Судить',
            'action_url': 'tournament:registration_adjudicator',
            'form': adjudicator_form,
            'tournament': tournament,
        }
    )


@csrf_protect
@ajax_request
@login_required(login_url=reverse_lazy('account_login'))
@access_by_status(name_page='team/adju. add')
def add_adjudicator(request, tournament):
    user = User.objects.filter(email__iexact=request.POST.get('email', '')).first()

    if not user:
        return json_response(MSG_JSON_BAD, MSG_USER_NOT_EXIST_p % request.POST.get('email', ''))

    if _registration_adjudicator(tournament, user):
        return json_response(MSG_JSON_OK, MSG_ADJUDICATOR_SUCCESS_REGISTERED_p % tournament.name)
    else:
        return json_response(MSG_JSON_BAD, MSG_ADJUDICATOR_ALREADY_REGISTERED_pp % (user.name(), tournament.name))


@login_required(login_url=reverse_lazy('account_login'))
@access_by_status(name_page='team/adju. edit')
def edit_adjudicator_list(request, tournament):
    return render(
        request,
        'tournament/edit_adjudicator_list.html',
        {
            'is_check_page': request.path == reverse('tournament:check_adjudicator_list', args=[tournament.id]),
            'chair_need': tournament.teamtournamentrel_set.filter(role=ROLE_MEMBER).count() // TEAM_IN_GAME,
            'user_tournament_rels': tournament.get_users(ADJUDICATOR_ROLES),
            'statuses': ADJUDICATOR_ROLES,
            'chair_role': ROLE_CHAIR,
            'tournament': tournament,
        }
    )


@csrf_protect
@ajax_request
@login_required(login_url=reverse_lazy('account_login'))
@access_by_status(name_page='team/adju. edit')
def adjudicator_role_update(request, tournament):
    rel = get_object_or_404(UserTournamentRel, pk=request.POST.get('rel_id', '0'))
    new_role = get_object_or_404(TournamentRole, pk=request.POST.get('new_role_id', '0'))
    if new_role not in ADJUDICATOR_ROLES:
        return json_response(MSG_JSON_BAD, MSG_BAD_ADJUDICATOR_ROLE)

    teams = get_teams_by_user(rel.user, rel.tournament)
    if new_role in [ROLE_CHAIR, ROLE_CHIEF_ADJUDICATOR, ROLE_WING] and teams:
        return json_response(
            MSG_JSON_BAD, MSG_USER_ALREADY_IS_MEMBER_pp % (rel.user.name(), teams[0].team.name)
        )

    rel.role = new_role
    rel.save()

    return json_response(MSG_JSON_OK, MSG_ADJUDICATOR_ROLE_CHANGE)


##################################
#   Management of adjudicator    #
##################################

@ensure_csrf_cookie
@login_required(login_url=reverse_lazy('account_login'))
@access_by_status(name_page='edit', only_owner=True)
def list_admin(request, tournament: Tournament):
    return render(
        request,
        'tournament/admin_list.html',
        {
            'admins': tournament.get_users([ROLE_ADMIN]),
            'owner': request.user,
            'tournament': tournament,
        }
    )


@csrf_protect
@ajax_request
@login_required(login_url=reverse_lazy('account_login'))
@access_by_status(name_page='edit', only_owner=True)
def add_admin(request, tournament):
    user = User.objects.filter(email__iexact=request.POST.get('email', '')).first()

    if not user:
        return json_response(
            MSG_JSON_BAD, MSG_USER_NOT_EXIST_p % request.POST.get('email', '')
        )

    admin_rel = UserTournamentRel.objects.get_or_create(user=user, tournament=tournament, role=ROLE_ADMIN)
    if not admin_rel[1]:
        return json_response(
            MSG_JSON_BAD, MSG_ADMIN_ALREADY_ADD_p % user.name()
        )

    return json_response(
        MSG_JSON_OK, {
            'rel_id': admin_rel[0].id,
            'name': user.name(),
        }
    )


@csrf_protect
@ajax_request
@login_required(login_url=reverse_lazy('account_login'))
@access_by_status(name_page='edit', only_owner=True)
def remove_admin(request, tournament):
    rel_id = request.POST.get('rel_id', '0')
    admin_rel = UserTournamentRel.objects.filter(pk=rel_id, role=ROLE_ADMIN).select_related('user')

    if not admin_rel.first():
        return json_response(MSG_JSON_BAD, MSG_ADMIN_NOT_EXIST)

    admin = admin_rel.first().user
    admin_rel.delete()

    return json_response(
        MSG_JSON_OK, MSG_ADMIN_REMOVE_p % admin.name()
    )


@csrf_protect
@ajax_request
@login_required(login_url=reverse_lazy('account_login'))
@access_by_status(name_page='edit', only_owner=True)
def change_owner(request, tournament):
    owner_rel = UserTournamentRel.objects.filter(user=request.user, tournament=tournament, role=ROLE_OWNER)
    admin_rel = UserTournamentRel.objects.filter(pk=request.POST.get('rel_id', '0'))

    if not admin_rel.first():
        return json_response(MSG_JSON_BAD, MSG_ADMIN_NOT_EXIST)

    owner_rel.update(role=ROLE_ADMIN)
    admin_rel.update(role=ROLE_OWNER)

    return json_response(
        MSG_JSON_OK, MSG_OWNER_CHANGED_p % admin_rel.first().user.name()
    )


##################################
#             Places             #
##################################

@ensure_csrf_cookie
@login_required(login_url=reverse_lazy('account_login'))
@access_by_status(name_page='edit')
def place_list(request, tournament):
    return render(
        request,
        'tournament/place_list.html',
        {
            'is_check_page': request.path == reverse('tournament:place_check', args=[tournament.id]),
            'places_need': tournament.teamtournamentrel_set.filter(role=ROLE_MEMBER).count() // TEAM_IN_GAME,
            'places': tournament.place_set.all(),
            'tournament': tournament,
        }
    )


@csrf_protect
@ajax_request
@login_required(login_url=reverse_lazy('account_login'))
@access_by_status(name_page='edit')
def place_update(request, tournament):
    place_id = request.POST.get('place_id', '')
    is_active = request.POST.get('is_active', '').lower() == 'true'
    if not tournament.place_set.filter(pk=place_id).exists():
        return json_response(MSG_JSON_BAD, 'Нет такой')

    tournament.place_set.filter(pk=place_id).update(is_active=is_active)

    return json_response(
        MSG_JSON_OK, is_active
    )


@csrf_protect
@ajax_request
@login_required(login_url=reverse_lazy('account_login'))
@access_by_status(name_page='edit')
def place_add(request, tournament):
    place_name = request.POST.get('place', '').strip()[:100]  # max length of place name
    place = tournament.place_set.get_or_create(place=place_name, tournament=tournament)
    if not place[1]:
        return json_response(MSG_JSON_BAD, 'уже есть')

    return json_response(
        MSG_JSON_OK, {
            'place_id': place[0].id,
            'name': place[0].place,
        }
    )


@csrf_protect
@ajax_request
@login_required(login_url=reverse_lazy('account_login'))
@access_by_status(name_page='edit')
def place_remove(request, tournament):
    place_id = request.POST.get('id', '')
    if not tournament.place_set.filter(pk=place_id).exists():
        return json_response(MSG_JSON_BAD, 'Нет такой')

    tournament.place_set.filter(pk=place_id).delete()

    return json_response(
        MSG_JSON_OK, 'ok'
    )


##################################
#          Custom Forms          #
##################################
from apps.tournament.consts import CUSTOM_FORM_TYPES
from apps.tournament.models import \
    CustomForm, \
    CustomFormAnswers, \
    CustomQuestion, \
    FeedbackAnswer
from .registration_forms import CustomFeedbackForm


@ensure_csrf_cookie
@login_required(login_url=reverse_lazy('account_login'))
@access_by_status(name_page='custom_questions')
def custom_form_edit(request, tournament, form_type):
    form = CustomForm.get_or_create(tournament, CUSTOM_FORM_TYPES[form_type])
    questions = CustomQuestion.objects.filter(form=form).select_related('alias').order_by('position')

    return render(
        request,
        'tournament/custom_form_edit.html',
        {
            'tournament': tournament,
            'form': form,
            'questions': questions,
            'required_aliases': REQUIRED_ALIASES,
            'actions': CUSTOM_FORM_AJAX_ACTIONS,
            'title': CUSTOM_FORM_QUESTIONS_TITLES[CUSTOM_FORM_TYPES[form_type]],
        }
    )


@csrf_protect
@ajax_request
@login_required(login_url=reverse_lazy('account_login'))
@access_by_status(name_page='custom_questions')
def custom_form_edit_field(request, tournament):
    form_id = int(request.POST.get('form_id', '0'))
    action = request.POST.get('action', '')

    form = CustomForm.objects.filter(pk=form_id).first()

    if not form or form.tournament != tournament:
        status = MSG_JSON_BAD
        message = 'Такой формы не найдено'
    elif action == CUSTOM_FORM_AJAX_ACTIONS['edit_question']:
        status, message = _form_edit_field(request, form)
    elif action == CUSTOM_FORM_AJAX_ACTIONS['remove_question']:
        status, message = _form_remove_field(request, form)
    elif action == CUSTOM_FORM_AJAX_ACTIONS['up_question']:
        status, message = _form_up_field(request, form)
    elif action == CUSTOM_FORM_AJAX_ACTIONS['down_question']:
        status, message = _form_down_field(request, form)
    else:
        status = MSG_JSON_BAD
        message = 'Чё надо то'

    return json_response(status, message)


def _form_edit_field(request, form: CustomForm):
    field_id = int(request.POST.get('question_id', 0))
    question = request.POST.get('question', '')
    comment = request.POST.get('comment', '')
    is_required = request.POST.get('is_required', '0') == '1'

    if not question:
        return MSG_JSON_BAD, 'Вопрос не может быть пустым'

    if field_id:
        field = form.customquestion_set.filter(pk=field_id).first()
        if not field:
            return MSG_JSON_BAD, 'Вопрос не найден'

        if field.alias in REQUIRED_ALIASES:
            return MSG_JSON_BAD, 'Этот вопрос является обязательным, его нельзя редактировать'

        field.question = question
        field.comment = comment
        field.required = is_required
        field.save()
        message = 'Вопрос сохранён'
    else:
        position = form.customquestion_set.latest('position').position + 1 if form.customquestion_set.count() else 1
        field = CustomQuestion.objects.create(
            question=question,
            comment=comment,
            position=position,
            required=is_required,
            form=form,
        )
        message = 'Вопрос добавлен'

    return MSG_JSON_OK, {
        'question_id': field.id,
        'message': message,
    }


def _form_remove_field(request, form: CustomForm):
    from django.db.models import F

    field_id = int(request.POST.get('question_id', 0))
    field = form.customquestion_set.filter(pk=field_id).first()
    if not field:
        return MSG_JSON_BAD, 'Вопрос не найден'

    if field.alias in REQUIRED_ALIASES:
        return MSG_JSON_BAD, 'Обязательные вопросы нельзя удалять'

    form.customquestion_set.filter(position__gt=field.position).update(position=F('position') - 1)
    field.delete()

    return MSG_JSON_OK, 'Вопрос удалён'


def _swap_field(field, prev_field):
    if not field or not prev_field:
        return MSG_JSON_BAD, 'Вопрос не найден'

    if prev_field.position + 1 != field.position:
        return MSG_JSON_BAD, 'Невозможно изменить порядок вопросов'

    field.position -= 1
    field.save()

    prev_field.position += 1
    prev_field.save()

    return MSG_JSON_OK, 'Изменения сохранены'


def _form_up_field(request, form: CustomForm):
    field_id = int(request.POST.get('question_id', 0))
    field = form.customquestion_set.filter(pk=field_id).first()

    prev_field_id = int(request.POST.get('prev_question_id', 0))
    prev_field = form.customquestion_set.filter(pk=prev_field_id).first()

    return _swap_field(field, prev_field)


def _form_down_field(request, form: CustomForm):
    field_id = int(request.POST.get('question_id', 0))
    field = form.customquestion_set.filter(pk=field_id).first()

    next_field_id = int(request.POST.get('next_question_id', 0))
    next_field = form.customquestion_set.filter(pk=next_field_id).first()

    return _swap_field(next_field, field)


@login_required(login_url=reverse_lazy('account_login'))
@access_by_status(name_page='custom_answers')
def custom_form_show_answers(request, tournament, form_type):
    custom_form = get_object_or_404(CustomForm, tournament=tournament, form_type=CUSTOM_FORM_TYPES[form_type])

    title = ''
    column_names = list(map(lambda x: x.question, custom_form.customquestion_set.all().order_by('position')))
    if custom_form.form_type == FORM_FEEDBACK_TYPE:
        column_names = [LBL_ROUND_FEEDBACK, LBL_CHAIR_FEEDBACK] + column_names
    column_values = []
    for custom_form_answers in CustomFormAnswers.objects.filter(form=custom_form).order_by('id'):
        answers = custom_form_answers.get_answers()
        column_values.append(list(map(lambda x: answers.get(x, ''), column_names)))

    return render(
        request,
        'tournament/custom_form_answers.html',
        {
            'tournament': tournament,
            'title': CUSTOM_FORM_ANSWERS_TITLES[CUSTOM_FORM_TYPES[form_type]],
            'column_names': column_names,
            'rows': column_values,
        }
    )


# ======

def show_profile(request, user_id):
    try:
        # not use get_object_or_404 because need select_related
        users = User.objects
        for name in ['university', 'university__city', 'university__country']:
            users = users.select_related(name)
        user = users.get(pk=user_id)
    except ObjectDoesNotExist:
        raise Http404('User with id %s not exist' % user_id)

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
            'is_owner': request.user.is_authenticated and user == request.user,
            'teams_objects': teams_rel,
            'adjudicators_objects': adjudicators_rel,
        }
    )


def edit_profile(request):
    if not request.user.is_authenticated:
        raise Http404
    is_success = False
    if request.method == 'POST':
        form = EditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            is_success = True
    else:
        form = EditForm(instance=request.user)
    return render(
        request,
        'account/signup.html',
        {
            'is_edit_form': True,
            'is_success': is_success,
            'user': request.user,
            'form': form,
        }
    )

@login_required(login_url=reverse_lazy('account_login'))
def connect_telegram(request):
    from django_telegrambot.apps import DjangoTelegramBot

    return redirect('https://telegram.me/%s?start=%s' % (
        DjangoTelegramBot.getBot().username,
        TelegramToken.generate(request.user).value
    ))


def show_tournaments_of_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    tournaments = Tournament.objects.select_related('status').annotate(
        m_count=Count(Case(
            When(teamtournamentrel__role=ROLE_MEMBER, then=1),
            output_field=IntegerField()
        ))
    ).filter(
        usertournamentrel__user=user,
        usertournamentrel__role__in=[ROLE_ADMIN, ROLE_OWNER]
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
            'objects': teams_rel,
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
            'objects': adjudicators_rel,
        }
    )


# ================================ main

def index(request):
    DAYS_TO_LEAVE_SHORT_LIST = 3
    is_short = request.GET.get('list', None) != 'all'
    tournaments = Tournament.objects.select_related('status').annotate(
        m_count=Count(Case(
            When(teamtournamentrel__role=ROLE_MEMBER, then=1),
            output_field=IntegerField()
        ))
    )
    if is_short:
        # TODO Возможно стоит всегда показывать свои турниры в списке
        tournaments = tournaments.filter(
            Q(status__in=[STATUS_STARTED, STATUS_PLAYOFF, STATUS_FINISHED])
            |
            Q(start_tour__gte=(date.today() - timedelta(days=DAYS_TO_LEAVE_SHORT_LIST)))
        )
    else:
        tournaments = tournaments.all()

    return render(
        request,
        'main/main.html',
        {
            'is_main_page': True,
            'is_short': is_short,
            'objects': paging(
                request, list(tournaments.order_by('-start_tour')), 15
            )
        }
    )


@login_required(login_url=reverse_lazy('account_login'))
@access_by_status(name_page='')
def team_feedback(request, tournament):
    rooms = get_rooms_by_user(tournament, request.user)
    if not rooms:
        return _show_message(request, MSG_USER_FEEDBACK_WITHOUT_ROUNDS)

    custom_form = CustomForm.objects.filter(tournament=tournament, form_type=FORM_FEEDBACK_TYPE).first()
    questions = CustomQuestion.objects.filter(form=custom_form).select_related('alias').order_by('position') \
        if custom_form \
        else None

    if not questions:
        return _show_message(request, MSG_FEEDBACK_WITHOUT_QUESTIONS)

    if request.method == 'POST':
        feedback_form = CustomFeedbackForm(questions, None, request.POST)
        if feedback_form.is_valid():
            round_id = int(request.POST.get('round', 0))
            answers_from_form = {}

            for room in rooms:
                if room.round.id == round_id:
                    answers_from_form = {
                        LBL_ROUND_FEEDBACK: room.round.number,
                        LBL_CHAIR_FEEDBACK: room.game.chair.get_full_name(),
                    }
                    break

            answers_from_form.update(feedback_form.get_answers(questions))

            feedback_answers = FeedbackAnswer.objects.get_or_create(
                user=request.user,
                round_id=int(request.POST.get('round', 0)),
                form=custom_form
            )
            feedback_answers[0].set_answers(answers_from_form)
            feedback_answers[0].save()
            # TODO add message
            return _show_message(request, MSG_FEEDBACK_SAVED)

    else:
        feedback_answers = FeedbackAnswer.objects.filter(user=request.user, round=rooms.last().round).first()
        feedback_form = CustomFeedbackForm(questions, feedback_answers.get_answers() if feedback_answers else None)

    return render(
        request,
        'tournament/team_feedback.html',
        {
            'rooms': rooms,
            'title': 'Обратная связь на судью',
            'submit_title': 'Оставить Feedback',
            'action_url': 'tournament:team_feedback',
            'form': feedback_form,
            'tournament': tournament,
        }
    )
