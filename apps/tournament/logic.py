import datetime
import random
import logging

from django.db.models import Q, Count
from django.core.exceptions import ObjectDoesNotExist
from .consts import *
from .messages import *
from .models import \
    Tournament,\
    TeamTournamentRel, \
    Round, \
    Room, \
    Game, \
    GameResult, \
    Motion, \
    User


class TeamRoundResult:
    def __init__(self,
                 place: int,
                 speaker_1: int,
                 speaker_2: int,
                 is_reversed: bool,
                 position: Position,
                 number: int,
                 is_closed: bool,
                 is_playoff: bool,
                 ):
        self.points = 4 - place if not is_playoff and place else place
        self.speaker_1 = speaker_1
        self.speaker_2 = speaker_2
        self.is_reversed = is_reversed
        self.position = position
        self.number = number
        self.is_closed = is_closed
        self.is_playoff = is_playoff


class TeamResult:

    def __init__(self, team, count_playoff_rounds):
        self.playoff_position = 0
        self.count_playoff_rounds = count_playoff_rounds
        self.show_all = True
        self.team = team
        self.rounds = []
        self.position = [0, 0, 0, 0]

    def add_empty_round(self, round_number):
        self.rounds.append(TeamRoundResult(0, 0, 0, False, Position.NONE, round_number, False, False))

    def add_playoff_round(self, other: TeamRoundResult):
        self.playoff_position = max(self.playoff_position, other.number + int(other.points))
        return self.rounds

    def add_round(self, other: TeamRoundResult):
        if len(self.rounds) + 1 == other.number:
            self.rounds.append(other)
        elif len(self.rounds) + 1 < other.number:
            for i in range(len(self.rounds) + 1, other.number):
                self.add_empty_round(i)
            self.rounds.append(other)
        elif len(self.rounds) + 1 > other.number:
            self.rounds[other.number - 1] = other

        if other.position != Position.NONE:
            self.position[other.position.value - 1] += 1

        return self.rounds

    def extract_speakers_result(self):
        speaker_1 = SpeakerResult(self.team, self.team.speaker_1)
        speaker_2 = SpeakerResult(self.team, self.team.speaker_2)

        for cur_round in self.rounds:
            speaker_1.add_round(cur_round.speaker_1, cur_round.number)
            speaker_2.add_round(cur_round.speaker_2, cur_round.number)

        return [speaker_1, speaker_2]

    def sum_points(self):
        return sum(list(map(lambda x: x.points * bool(self.show_all or not x.is_closed), self.rounds)))

    def sum_speakers(self):
        return 0 if not self.show_all \
            else sum(list(map(lambda x: x.speaker_1 + x.speaker_2, self.rounds)))

    def get_position_weight(self, position_index):
        return self.position[position_index] * 2 + 1

    def __gt__(self, other):
        return self.sum_points() > other.sum_points() \
            or self.sum_points() == other.sum_points() and self.sum_speakers() > other.sum_speakers()

    def __lt__(self, other):
        return self.sum_points() < other.sum_points() \
            or self.sum_points() == other.sum_points() and self.sum_speakers() < other.sum_speakers()

    def __str__(self):
        return "(%s) %s points:%s speakers:%s" % (self.team.id, self.team.name, self.sum_points(), self.sum_speakers())


class SpeakerResult:

    def __init__(self, team, user):
        self.team = team
        self.user = user
        self.points = []

    def add_round(self, points, round_number):
        if len(self.points) + 1 == round_number:
            self.points.append(points)
        elif len(self.points) + 1 < round_number:
            for i in range(len(self.points) + 1, round_number):
                self.points.append(0)
            self.points.append(points)
        elif len(self.points) + 1 > round_number:
            self.points[round_number - 1] = points

        return self

    def sum_points(self):
        return sum(self.points)

    def __gt__(self, other):
        return self.sum_points() > other.sum_points()

    def __eq__(self, other):
        return self.sum_points() == other.sum_points()

    def __lt__(self, other):
        return self.sum_points() < other.sum_points()

    def __str__(self):
        return "|%s| %s <%s> : %s" % (self.user.id, self.user.name(), self.team.name, self.sum_points())


def _get_last_round(tournament: Tournament):
    return Round.objects.filter(
        tournament=tournament,
        is_playoff=(tournament.status == STATUS_PLAYOFF),
        number__gt=0
    ).order_by('-number').first()


def _get_temp_round(tournament: Tournament) -> Round:
    return Round.objects.filter(
        tournament=tournament,
        is_playoff=True,
        number=-1
    ).first()


def _count_playoff_rounds_in_tournament(teams_in_round: int):
    result = 0
    while teams_in_round // 2 >= 2:
        result += 1
        teams_in_round /= 2
    return result


def _filter_tab(tab: [TeamResult], tournament: Tournament, roles: [TournamentRole]):
    teams = list(map(lambda x: x.team, tournament.get_teams(roles)))
    new_tab = list(filter(lambda x: x.team in teams, tab))
    teams_in_tab = list(map(lambda x: x.team, new_tab))
    for team in teams:
        if team in teams_in_tab:
            continue
        team_results = TeamResult(team, _count_playoff_rounds_in_tournament(tournament.count_teams_in_break))
        for i in range(tournament.cur_round):
            team_results.add_empty_round(i)
        new_tab.append(team_results)

    return new_tab


def _check_duplicate_role(role: TournamentRole, rel: TeamTournamentRel, user: User) -> [TeamTournamentRel]:
    return TeamTournamentRel.objects.filter(
        ~Q(id=rel.id),
        Q(team__speaker_1=user) | Q(team__speaker_2=user),
        tournament=rel.tournament,
        role=role
    )


##############################################
#              Generate rounds              ##
##############################################

def _generate_random_round(tournament: Tournament, cur_round: Round):
    teams = list(tournament.get_teams([ROLE_MEMBER]).order_by('?'))
    chair = list(tournament.get_users([ROLE_CHAIR]).order_by('?'))
    place = list(tournament.place_set.filter(is_active=True).order_by('?'))

    for i in range(len(teams) // TEAM_IN_GAME):
        game = Game.objects.create(
            og=teams.pop().team,
            oo=teams.pop().team,
            cg=teams.pop().team,
            co=teams.pop().team,
            chair=chair.pop().user,
            date=datetime.datetime.now(),
            motion=cur_round.motion
        )
        Room.objects.create(
            game=game,
            round=cur_round,
            number=i,
            place=place.pop()
        )


def _generate_round(tournament: Tournament, cur_round: Round):
    import itertools

    MAX_POINTS = 1 + POINTS_OF_FIRST_PLACE * (cur_round.number - 1)

    tab = _filter_tab(get_tab(tournament), tournament, [ROLE_MEMBER])

    team_by_points = [[] for _ in range(MAX_POINTS)]
    for i in tab:
        team_by_points[i.sum_points()].append(i)

    for i in team_by_points:
        random.shuffle(i)

    tab = [val for sub_list in reversed(team_by_points) for val in sub_list]

    pools = []
    while tab:
        best_weight = 0
        pool = {
            'game': None,
            'max_point': tab[0].sum_points(),
            'min_point': tab[TEAM_IN_GAME - 1].sum_points(),
        }
        # Сумма квадратов оптимальных (min) позиций
        break_weight = sum(map(
            lambda y: y ** 2,
            map(
                lambda x: min(x.position),
                tab[:TEAM_IN_GAME]
            )
        ))
        for i in itertools.permutations(tab[:TEAM_IN_GAME]):
            weight = sum(map(
                lambda x: x ** 2,
                [i[0].position[0], i[1].position[1], i[2].position[2], i[3].position[3]]
            ))
            if not pool['game'] or best_weight > weight:
                best_weight = weight
                pool['game'] = list(i)
                if break_weight == best_weight:
                    break

        pools.append(pool)
        tab = tab[TEAM_IN_GAME:]

    # [1-4 => 1, 5-8 => 2, 9-12 => 3, ...]
    max_games_in_position = cur_round.number // TEAM_IN_GAME + int(cur_round.number % TEAM_IN_GAME > 0)
    bad = [[] for _ in range(MAX_POINTS)]
    good = [[] for _ in range(MAX_POINTS)]

    for i in range(len(pools)):
        pool = pools[i]
        for j in range(TEAM_IN_GAME):
            team = pool['game'][j]

            can = []
            for k in range(len(team.position)):
                if team.position[k] < max_games_in_position:
                    can.append(k)

            x = {
                'pool': i,
                'team': j,
                'can': set(can),
            }
            if team.position[j] >= max_games_in_position:
                bad[team.sum_points()].append(x)
            else:
                good[team.sum_points()].append(x)

    for k in range(MAX_POINTS):
        i = 0
        while bad[k] and i < len(bad[k]):
            replace_with = -1
            for j in range(i + 1, len(bad[k])):
                if bad[k][i]['team'] in bad[k][j]['can'] and bad[k][j]['team'] in bad[k][i]['can']:
                    replace_with = j
                    break

            if replace_with >= 0:
                p1 = bad[k][i]['pool']
                p2 = bad[k][replace_with]['pool']
                t1 = bad[k][i]['team']
                t2 = bad[k][replace_with]['team']
                pools[p1]['game'][t1], pools[p2]['game'][t2] = pools[p2]['game'][t2], pools[p1]['game'][t1]

                good[k].append({
                    'pool': p1,
                    'team': t1,
                    'can': bad[k][replace_with]['can'],
                })
                good[k].append({
                    'pool': p2,
                    'team': t2,
                    'can': bad[k][i]['can'],
                })

                bad[k] = bad[k][:i] + bad[k][i + 1:replace_with] + bad[k][replace_with + 1:]
                continue

            for j in range(len(good[k])):
                if bad[k][i]['team'] in good[k][j]['can'] and good[k][j]['team'] in bad[k][i]['can']:
                    replace_with = j
                    break

            if replace_with >= 0:
                p1 = bad[k][i]['pool']
                p2 = good[k][replace_with]['pool']
                t1 = bad[k][i]['team']
                t2 = good[k][replace_with]['team']
                pools[p1]['game'][t1], pools[p2]['game'][t2] = pools[p2]['game'][t2], pools[p1]['game'][t1]

                temp = good[k][replace_with]['can']
                good[k][replace_with]['can'] = bad[k][i]['can']
                good[k].append({
                    'pool': p1,
                    'team': t1,
                    'can': temp,
                })
                bad[k] = bad[k][:i] + bad[k][i + 1:]
                continue

            i += 1

    chair = list(tournament.get_users([ROLE_CHAIR]).order_by('?'))
    place = list(tournament.place_set.filter(is_active=True).order_by('?'))
    for i in range(len(pools)):
        game = Game.objects.create(
            og=pools[i]['game'][0].team,
            oo=pools[i]['game'][1].team,
            cg=pools[i]['game'][2].team,
            co=pools[i]['game'][3].team,
            chair=chair.pop().user,
            date=datetime.datetime.now(),
            motion=cur_round.motion
        )
        Room.objects.create(
            game=game,
            round=cur_round,
            number=i,
            place=place.pop()
        )


def _generate_first_playoff_round(tournament: Tournament, new_round: Round):
    temp_round = _get_temp_round(tournament)

    if not temp_round:
        return 'Нет команд, сделавших брейк. Объявите брейк'

    for room in Room.objects.filter(round=temp_round):
        game = room.game
        game.pk = None
        game.motion = new_round.motion
        game.date = datetime.datetime.now()
        game.save()
        room.pk = None
        room.round = new_round
        room.game = game
        room.save()


def _generate_playoff_round(tournament: Tournament, cur_round: Round):
    positions = [
        ['og_id', 'og'],
        ['oo_id', 'oo'],
        ['cg_id', 'cg'],
        ['co_id', 'co'],
    ]

    chair = list(tournament.get_users([ROLE_CHAIR]).order_by('?'))
    place = list(tournament.place_set.filter(is_active=True).order_by('?'))

    queryset = Room.objects.filter(
        round__tournament=tournament,
        round__is_playoff=True,
        round__number=cur_round.number - 1
    )
    for i in ['round', 'game', 'game__gameresult', 'game__gameresult__playoffresult']:
        queryset = queryset.select_related(i)

    result_prev_round = list(queryset)
    if len(result_prev_round) < 2:
        return 'Финал турнира уже сыгран. Завершите турнир и опубликуйте результаты'

    teams_id = []
    for room in result_prev_round:
        for position in positions:
            if getattr(room.game.gameresult.playoffresult, position[1]):
                teams_id.append(getattr(room.game, position[0]))

    for i in range(len(teams_id) // TEAM_IN_GAME):
        teams_id_in_room = teams_id[:4]
        teams_id = teams_id[4:]
        random.shuffle(teams_id_in_room)
        game = Game.objects.create(
            og_id=teams_id_in_room.pop(),
            oo_id=teams_id_in_room.pop(),
            cg_id=teams_id_in_room.pop(),
            co_id=teams_id_in_room.pop(),
            chair=chair.pop().user,
            date=datetime.datetime.now(),
            motion=cur_round.motion
        )
        Room.objects.create(
            game=game,
            round=cur_round,
            number=i,
            place=place.pop()
        )


##############################################
#                  Public                   ##
##############################################

def can_change_team_role(rel: TeamTournamentRel, role: TournamentRole) -> [bool, str]:

    if role not in [ROLE_IN_TAB, ROLE_MEMBER]:
        return [True, '']

    if _check_duplicate_role(role, rel, rel.team.speaker_1):
        return [False, '%s уже участвует в турнире в другой команде' % rel.team.speaker_1.name()]

    if _check_duplicate_role(role, rel, rel.team.speaker_2):
        return [False, '%s уже участвует в турнире в другой команде' % rel.team.speaker_1.name()]

    return [True, '']


def check_games_results_exists(games: [Game]):
    return GameResult.objects.filter(game__in=games).count()


def check_final(tournament: Tournament):
    if tournament.status == STATUS_PLAYOFF and len(get_rooms_from_last_round(tournament)) == 1:
        return MSG_FINAL_ALREADY_EXIST

    return None


def check_last_round_results(tournament: Tournament):
    # TODO use count .annotate(count_game=Count('game_id'), count_results=Count('game__gameresult__id')) \
    rooms = Room.objects.filter(round=_get_last_round(tournament))\
        .select_related('game')\
        .select_related('game__gameresult')
    for room in rooms:
        try:
            room.game.gameresult
        except AttributeError:
            return 'Введите результаты последнего раунда'

    return None


def check_teams_and_adjudicators(tournament: Tournament):
    if tournament.status == STATUS_STARTED:
        count_teams = tournament.teamtournamentrel_set.filter(role=ROLE_MEMBER).count()
        if count_teams % TEAM_IN_GAME:
            return MSG_NEED_TEAMS_p % count_teams
        count_rooms = count_teams // TEAM_IN_GAME
    else:
        last_round = _get_last_round(tournament)
        temp_round = _get_temp_round(tournament)
        if last_round:
            count_rooms = Room.objects.filter(round=last_round).count() // 2
        elif temp_round:
            count_rooms = Room.objects.filter(round=temp_round).count()
        else:
            return None

    count_adjudicator = tournament.usertournamentrel_set.filter(role=ROLE_CHAIR).count()
    count_places = tournament.place_set.filter(is_active=True).count()

    return MSG_NEED_ADJUDICATOR if count_rooms > count_adjudicator \
        else MSG_NEED_PLACE if count_rooms > count_places \
        else None


def generate_next_round(tournament: Tournament, new_round: Round):
    """
    round - не сохранённый объект из формы
    """
    new_round.tournament = tournament
    new_round.is_public = False
    new_round.is_playoff = tournament.status == STATUS_PLAYOFF

    if tournament.status == STATUS_STARTED:
        new_round.number = tournament.round_number_inc()
        new_round.save()
        if tournament.cur_round == 1:
            return _generate_random_round(tournament, new_round)
        else:
            return _generate_round(tournament, new_round)

    elif tournament.status == STATUS_PLAYOFF:
        last_playoff_round = _get_last_round(tournament)
        if last_playoff_round:
            new_round.number = last_playoff_round.number + 1
            new_round.save()
            return _generate_playoff_round(tournament, new_round)
        else:
            new_round.number = 1
            new_round.save()
            return _generate_first_playoff_round(tournament, new_round)

    else:
        return 'Неверный статус турнира'


def generate_playoff(tournament: Tournament, teams: list):

    def _generate_playoff_position(count: int):
        result = [1]
        while len(result) != count:
            print(result)
            l = len(result)
            new_l = l * 2
            new_result = [0] * new_l
            for i in range(l):
                new_result[i * 2] = result[i]
                new_result[i * 2 + 1] = new_l - result[i] + 1
            result = new_result
        return result

    positions = list(map(lambda x: x - 1, _generate_playoff_position(tournament.count_teams_in_break)))
    motion = Motion.objects.create(motion='temp')
    chair = list(tournament.get_users([ROLE_CHAIR]).order_by('?'))
    place = list(tournament.place_set.filter(is_active=True).order_by('?'))

    new_round = Round.objects.create(
        tournament=tournament,
        motion=motion,
        number=-1,
        start_time=datetime.datetime.now(),
        is_playoff=True,
    )
    for i in range(len(teams) // TEAM_IN_GAME):
        game = Game.objects.create(
            og=teams[positions[i * TEAM_IN_GAME]],
            oo=teams[positions[i * TEAM_IN_GAME + 1]],
            cg=teams[positions[i * TEAM_IN_GAME + 2]],
            co=teams[positions[i * TEAM_IN_GAME + 3]],
            chair=chair.pop().user,
            date=datetime.datetime.now(),
            motion=motion,
        )
        Room.objects.create(
            game=game,
            round=new_round,
            number=i,
            place=place.pop()
        )


def get_games_and_results(rooms: [Room]):
    results = []
    for room in rooms:
        try:
            result = room.game.gameresult.qualificationresult if not room.round.is_playoff \
                else room.game.gameresult.playoffresult
        except ObjectDoesNotExist:
            result = None

        results.append({
            'game': room.game,
            'result': result
        })
    return results


def get_motions(tournament: Tournament):
    motions = {
        'qualification': [],
        'playoff': [],
    }

    # Выборка тем и инфослайдов, № раунда для заголовка в отборочных, колличество румов для заголовка в плейофф
    # и количество результатор, для опубликования этой темы в тэбе
    # >>>
    query_set = Room.objects.filter(round__tournament=tournament, round__number__gt=0) \
        .values(
            'round__motion__motion', 'round__motion__infoslide',
            'round__number', 'round__is_playoff', 'round__motion__id'
        ) \
        .annotate(count_game=Count('game_id'), count_results=Count('game__gameresult__id')) \
        .order_by('round__number', 'round__is_playoff')
    # >>>

    for motion in query_set:
        if not motion['count_results']:
            continue

        new_motion = {
            'motion': motion['round__motion__motion'],
            'infoslide': motion['round__motion__infoslide'],
            'id': motion['round__motion__id'],
            'is_playoff': motion['round__is_playoff'],
        }
        if motion['round__is_playoff']:
            new_motion['number'] = 'Финал' \
                if motion['count_game'] == 1 \
                else '1/%s' % motion['count_game']
            motions['playoff'].append(new_motion)
        else:
            new_motion['number'] = 'Раунд ' + str(motion['round__number'])
            motions['qualification'].append(new_motion)

    return motions['qualification'] + motions['playoff']


def get_all_rounds_and_rooms(tournament: Tournament):
    results = []
    games = []

    # TODO Добавить .only() и убрать ненужные поля
    # TODO playoffresult
    rooms = Room.objects.filter(round__tournament=tournament, round__is_playoff=False)
    rooms = __include_room_related_models(rooms)

    for room in rooms.order_by('round_id', 'number'):

        try:  # TODO Убрать это
            room.game.gameresult
        except AttributeError:
            continue

        if not results or results[-1]['round'] != room.round:
            results.append({
                'round': room.round,
                'rooms': [],
            })

        results[-1]['rooms'].append({
            'game': room.game,
            'result': room.game.gameresult.qualificationresult,
        })
        games.append(room.game)

    return results


def get_rooms_from_last_round(tournament: Tournament, shuffle=False, chair=None) -> [Room]:
    room = Room.objects.filter(round=_get_last_round(tournament))
    if chair:
        room = room.filter(game__chair=chair)

    room = __include_room_related_models(room)

    return room.order_by('id') if not shuffle else room.order_by('?')


def get_tab(tournament: Tournament):
    """
    TODO Вынести класс tournament в отдельный файл и этот метот в этот класс
    :param tournament:
    :return:
    """
    teams = {}

    rooms = Room.objects.filter(round__tournament=tournament)
    rooms = __include_room_related_models(rooms)

    count_playoff_rounds = 0
    temp_round = _get_temp_round(tournament)
    if temp_round:
        count_playoff_rounds = _count_playoff_rounds_in_tournament(temp_round.room_set.count() * TEAM_IN_GAME)

    for room in rooms.order_by('round_id', 'number'):

        # TODO Убрать это
        try:
            room.game.gameresult
        except AttributeError:
            continue

        if room.round.is_playoff:
            game_result = room.game.gameresult.playoffresult
        else:
            game_result = room.game.gameresult.qualificationresult

        game_result.game = room.game

        for position in [
            [game_result.get_og_result(), Position.OG],
            [game_result.get_oo_result(), Position.OO],
            [game_result.get_cg_result(), Position.CG],
            [game_result.get_co_result(), Position.CO],
        ]:
            team_result = TeamRoundResult(
                position[0]['place'],
                position[0]['speaker_1'],
                position[0]['speaker_2'],
                position[0]['revert'],
                position[1],
                room.round.number,
                room.round.is_closed,
                room.round.is_playoff
            )

            if position[0]['team'].id not in teams.keys():
                teams[position[0]['team'].id] = TeamResult(position[0]['team'], count_playoff_rounds)

            if room.round.is_playoff:
                teams[position[0]['team'].id].add_playoff_round(team_result)
            else:
                teams[position[0]['team'].id].add_round(team_result)

    return list(teams.values())


def get_teams_by_user(user: User, tournament: Tournament, roles=[ROLE_MEMBER]):
    return TeamTournamentRel.objects.filter(
        Q(team__speaker_1=user) | Q(team__speaker_2=user),
        tournament=tournament,
        role__in=roles
    )


def publish_last_round(tournament: Tournament):
    last_round = _get_last_round(tournament)
    if not last_round:
        return False

    last_round.publish()
    return True


def remove_last_round(tournament: Tournament):
    last_round = _get_last_round(tournament)
    if not last_round:
        return False

    for room in Room.objects.filter(round=last_round):
        room.game.delete()

    if not last_round.is_playoff:
        tournament.round_number_dec()

    last_round.delete()
    return True


def remove_playoff(tournament: Tournament):
    last_round = _get_last_round(tournament)
    if last_round:
        return False

    temp_round = _get_temp_round(tournament)
    if temp_round:
        temp_round.delete()

    return True


def get_rooms_by_user(tournament: Tournament, user: User) -> [Room]:
    team_rel = tournament.teamtournamentrel_set.filter(
        Q(team__speaker_1=user) | Q(team__speaker_2=user),
        role=ROLE_MEMBER
    )

    if not team_rel.count():
        return []
    elif team_rel.count() > 1:
        logging.getLogger('TeamFeedback').error(
            'There %d actual teams for user (%d) in tournament (%d)' % (team_rel.count(), user.id, tournament.id)
        )

    team = team_rel.first().team

    return Room.objects.filter(
        Q(game__og=team) | Q(game__oo=team) | Q(game__cg=team) | Q(game__co=team),
        round__number__gt=0,
        round__is_playoff=False
    ).select_related('game', 'game__chair', 'round').order_by('round__number')


def user_can_edit_tournament(tournament: Tournament, user: User, only_owner=False):
    roles = [ROLE_OWNER] if only_owner else [ROLE_OWNER, ROLE_ADMIN, ROLE_CHIEF_ADJUDICATOR]
    return user.is_authenticated and tournament.usertournamentrel_set.filter(
        user=user,
        role__in=roles
    ).count()


def __include_room_related_models(queryset):
    for i in ['game', 'place', 'round', 'game__gameresult', 'game__chair']:
        queryset = queryset.select_related(i)
    for i in ['playoffresult', 'qualificationresult']:
        queryset = queryset.select_related('game__gameresult__%s' % i)
    for i in ['og', 'oo', 'cg', 'co']:
        queryset = queryset.select_related('game__%s' % i)
        for j in ['speaker_1', 'speaker_2']:
            queryset = queryset.select_related('game__%s__%s' % (i, j))

    return queryset
