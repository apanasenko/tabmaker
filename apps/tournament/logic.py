import random
import datetime
import itertools
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from apps.game.models import\
    Game, \
    GameResult
from apps.team.models import Team
from apps.motion.models import Motion
from .db_execute import \
    get_teams_result_list, \
    get_motion_list
from .consts import *
from .messages import *
from .models import \
    Tournament,\
    TeamTournamentRel, \
    UserTournamentRel, \
    Round,\
    Room
from apps.profile.models import User


class TeamRoundResult:
    def __init__(self,
                 points: int,
                 speaker_1: int,
                 speaker_2: int,
                 is_reversed: bool,
                 position: Position,
                 number: int,
                 is_closed: bool,
                 is_playoff: bool,
                 ):
        self.points = points
        self.speaker_1 = speaker_1
        self.speaker_2 = speaker_2
        self.is_reversed = is_reversed
        self.position = position
        self.number = number
        self.is_closed = is_closed
        self.is_playoff = is_playoff


class TeamResult:

    def __init__(self, team_id, count_playoff_rounds):
        self.playoff_position = 0
        self.count_playoff_rounds = count_playoff_rounds
        self.show_all = True
        self.team = Team.objects.get(pk=team_id)
        self.rounds = []
        self.position = [0, 0, 0, 0]

    def add_empty_round(self, round_number):
        self.rounds.append(TeamRoundResult(0, 0, 0, False, Position.NONE, round_number, False, False))

    def add_round(self, other: TeamRoundResult):
        if other.is_playoff:
            is_inc_position = other.number < self.count_playoff_rounds and other.points >= POINTS_OF_SECOND_PLACE \
                or other.points == POINTS_OF_FIRST_PLACE
            self.playoff_position = max(self.playoff_position, other.number + int(is_inc_position))
            return self.rounds

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
        return sum(list(map(lambda x: x.points * int(self.show_all or not x.is_closed), self.rounds)))

    def sum_speakers(self):
        return sum(list(map(lambda x: (x.speaker_1 + x.speaker_2) * int(self.show_all), self.rounds)))

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
    last_rounds = Round.objects.filter(
        tournament=tournament,
        is_playoff=(tournament.status == STATUS_PLAYOFF),
        number__gt=0
    ).order_by('-number')
    return None if not last_rounds else last_rounds[0]


def _get_temp_round(tournament: Tournament):
    temp_round = Round.objects.filter(
        tournament=tournament,
        is_playoff=True,
        number=-1
    )
    return None if not temp_round else temp_round[0]


def _count_playoff_rounds_in_tournament(teams_in_round: int):
    result = 0
    while teams_in_round // 2 >= 2:
        result += 1
        teams_in_round /= 2
    return result


def _filter_tab(tab: [TeamResult], tournament: Tournament, roles: [TournamentRole]):
    teams = list(map(lambda x: x.team, tournament.teamtournamentrel_set.filter(role__in=roles)))
    new_tab = list(filter(lambda x: x.team in teams, tab))
    teams_in_tab = list(map(lambda x: x.team, new_tab))
    for team in teams:
        if team in teams_in_tab:
            continue
        team_results = TeamResult(team.id, _count_playoff_rounds_in_tournament(tournament.count_teams_in_break))
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
    teams = list(tournament.teamtournamentrel_set.filter(role=ROLE_MEMBER))
    chair = list(tournament.usertournamentrel_set.filter(role=ROLE_CHAIR))

    random.shuffle(chair)
    random.shuffle(teams)
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
            number=i
        )


def _generate_round(tournament: Tournament, cur_round: Round):

    tab = sorted(_filter_tab(get_tab(tournament), tournament, [ROLE_MEMBER]), reverse=True)

    def find_best_team_in_position(teams, need_positions):
        positions_priority = {}
        max_weight = 0

        def a(_positions, find_result):
            if not _positions:
                find_teams = list(find_result.values())
                for ii in range(len(find_teams)):
                    for j in range(ii + 1, len(find_teams)):
                        if find_teams[ii].team.id == find_teams[j].team.id:
                            return 0, []

                cur_sum = 0
                for key, value in find_result.items():
                    cur_sum += value.get_position_weight(key)
                return cur_sum, dict(find_result)

            position = _positions.pop()
            best_sum = 0
            best_position = []
            for team in positions_priority[position]:
                if team.get_position_weight(position) > max_weight:
                    break
                find_result[position] = team
                cur_sum, cur_position = a(set(_positions), find_result)
                if cur_sum and (not best_sum or best_sum > cur_sum):
                    best_sum = cur_sum
                    best_position = cur_position

            return best_sum, best_position

        for k in need_positions:
            positions_priority[k] = sorted(teams, key=lambda x: x.get_position_weight(k))

        find_sum = 0
        find_position = []
        while not find_sum:
            max_weight = max_weight * 2 + 1
            find_sum, find_position = a(set(need_positions), {})
        return find_position

    def _get_teams_with_eq_points(need_position):
        k = 0
        while k + 1 < len(tab) and tab[0].sum_points() == tab[k].sum_points():
            k += 1

        team_by_position = find_best_team_in_position(tab[:k], need_position)
        cur_positions = []
        cur_pool = []
        for key, value in team_by_position.items():
            cur_positions += [key]
            cur_pool += [value]
            tab.remove(value)

        return cur_pool, cur_positions

    def _find_best_position(_pool, need_position):
        n = len(_pool)
        best_positions = list(range(n))
        best_sum = sum(list(map(lambda x: _pool[x].get_position_weight(best_positions[x]), range(n))))

        for _positions in itertools.permutations(need_position, n):
            cur_sum = sum(list(map(lambda x: _pool[x].get_position_weight(_positions[x]), range(n))))
            if cur_sum < best_sum:
                best_sum = cur_sum
                best_positions = _positions

        return best_positions

    games = []
    while tab:

        if len(tab) == 4 or tab[3].sum_points() > tab[4].sum_points():
            pool = tab[:4]
            tab = tab[4:]
            positions = list(_find_best_position(pool, (0, 1, 2, 3)))
        elif tab[0].sum_points() > tab[4].sum_points():
            i = 3
            while tab[i - 1].sum_points() == tab[4].sum_points():
                i -= 1
            head_pool = tab[:i]
            tab = tab[i:]
            head_positions = _find_best_position(head_pool, (0, 1, 2, 3))

            tail_pool, tail_positions = _get_teams_with_eq_points({0, 1, 2, 3} - set(head_positions))
            positions = list(head_positions) + tail_positions
            pool = head_pool + tail_pool
        else:
            pool, positions = _get_teams_with_eq_points({0, 1, 2, 3})

        games.append({
            'pool': pool,
            'positions': positions
        })

    chair = list(tournament.usertournamentrel_set.filter(role=ROLE_CHAIR))
    random.shuffle(chair)
    for i in range(len(games)):
        positions = dict(zip(games[i]['positions'], games[i]['pool']))
        game = Game.objects.create(
            og=positions[0].team,
            oo=positions[1].team,
            cg=positions[2].team,
            co=positions[3].team,
            chair=chair.pop().user,
            date=datetime.datetime.now(),
            motion=cur_round.motion
        )
        Room.objects.create(
            game=game,
            round=cur_round,
            number=i
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

    chair = list(tournament.usertournamentrel_set.filter(role=ROLE_CHAIR))
    random.shuffle(chair)

    result_prev_round = get_teams_result_list(
        """
        WHERE round.tournament_id = %s
          AND round.is_playoff = %s
          AND round.number = %s
        ORDER BY room.number
        """,
        [
            tournament.id,
            True,
            cur_round.number - 1,
            ]
    )

    if len(result_prev_round) < 2:
        return 'Финал турнира уже сыгран. Завершите турнир и опубликуйте результаты'

    teams_id = []
    for room in result_prev_round:
        for position in positions:
            if room[position[1]] in [1, 2]:
                teams_id.append(room[position[0]])

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
            number=i
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


def check_final(tournament: Tournament):
    if tournament.status == STATUS_PLAYOFF and len(get_rooms_from_last_round(tournament)) == 1:
        return MSG_FINAL_ALREADY_EXIST

    return None


def check_last_round_results(tournament: Tournament):
    for room in Room.objects.filter(round=_get_last_round(tournament)):
        if not GameResult.objects.filter(game=room.game).exists():
            return 'Введите результаты последнего раунда'

    return None


def check_teams_and_adjudicators(tournament: Tournament):
    count_teams = tournament.teamtournamentrel_set.filter(role=ROLE_MEMBER).count()
    count_adjudicator = tournament.usertournamentrel_set.filter(role=ROLE_CHAIR).count()

    return MSG_NEED_TEAMS if count_teams % TEAM_IN_GAME \
        else MSG_NEED_ADJUDICATOR if count_teams // TEAM_IN_GAME > count_adjudicator \
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
    chair = list(tournament.usertournamentrel_set.filter(role=ROLE_CHAIR))
    random.shuffle(chair)
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
            motion=motion
        )
        Room.objects.create(
            game=game,
            round=new_round,
            number=i
        )


def get_games_and_results(rooms: [Room]):
    results = []
    for room in rooms:
        try:
            result = GameResult.objects.get(game=room.game)
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

    for motion in get_motion_list(tournament.id):
        new_motion = {
            'motion': motion['motion'],
            'infoslide': motion['infoslide'],
        }
        if motion['is_playoff']:
            new_motion['number'] = 'Финал' \
                if motion['count'] == 1 \
                else '1/%s' % motion['count']
            motions['playoff'].append(new_motion)
        else:
            new_motion['number'] = 'Раунд ' + str(motion['number'])
            motions['qualification'].append(new_motion)

    return motions['qualification'] + motions['playoff']


def get_all_rounds_and_rooms(tournament: Tournament):
    results = []
    games = []

    # Выборка всех связных объектов
    # >>>
    # TODO Добавить .only() и убрать ненужные поля
    queryset = Room.objects.filter(round__tournament=tournament, round__is_playoff=False)
    for i in ['round', 'game', 'game__chair']:
        queryset = queryset.select_related(i)
    for i in ['og', 'oo', 'cg', 'co']:
        queryset = queryset.select_related('game__%s' % i)
        for j in ['speaker_1', 'speaker_2']:
            queryset = queryset.select_related('game__%s__%s' % (i, j))
    queryset = queryset.select_related('game__gameresult')
    # <<<
    for i in queryset.order_by('round_id', 'number'):

        if not results or results[-1]['round'] != i.round:
            results.append({
                'round': i.round,
                'rooms': [],
            })

        results[-1]['rooms'].append({
            'game': i.game,
            'result': i.game.gameresult,
        })
        games.append(i.game)

    return results


def get_rooms_from_last_round(tournament: Tournament, shuffle=False):
    room = Room.objects.filter(round=_get_last_round(tournament))
    return room if not shuffle else room.order_by('?')


def get_rooms_by_chair_from_last_round(tournament: Tournament, user: User) -> Room:
    return Room.objects.filter(round=_get_last_round(tournament), game__chair=user)


def get_tab(tournament: Tournament):
    positions = [
        ['og_id', 'og', 'pm', 'dpm', 'og_rev', Position.OG],
        ['oo_id', 'oo', 'lo', 'dlo', 'oo_rev', Position.OO],
        ['cg_id', 'cg', 'mg', 'gw', 'cg_rev', Position.CG],
        ['co_id', 'co', 'mo', 'ow', 'co_rev', Position.CO],
    ]
    teams = {}
    for game in get_teams_result_list('WHERE round.tournament_id = %s', [tournament.id]):
        for position in positions:
            team_result = TeamRoundResult(
                4 - int(game[position[1]]),
                int(game[position[2]]),
                int(game[position[3]]),
                bool(game[position[4]]),
                position[5],
                int(game['number']),
                bool(game['is_closed']),
                bool(game['is_playoff'])
            )
            team_id = game[position[0]]
            if team_id not in teams.keys():
                teams[team_id] = TeamResult(team_id, _count_playoff_rounds_in_tournament(tournament.count_teams_in_break))

            teams[team_id].add_round(team_result)

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


def user_can_edit_tournament(tournament: Tournament, user: User):
    return user.is_authenticated() and 0 < len(UserTournamentRel.objects.filter(
        tournament=tournament,
        user=user,
        role__in=[ROLE_OWNER, ROLE_ADMIN, ROLE_CHIEF_ADJUDICATOR]
    ))
