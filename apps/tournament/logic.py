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
from .models import \
    Tournament,\
    TeamTournamentRel, \
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
                 is_closed: bool
                 ):
        self.points = points
        self.speaker_1 = speaker_1
        self.speaker_2 = speaker_2
        self.is_reversed = is_reversed
        self.position = position
        self.number = number
        self.is_closed = is_closed


class TeamResult:

    def __init__(self, team_id):
        self.show_all = True
        self.team = Team.objects.get(pk=team_id)
        self.rounds = []
        self.position = [0, 0, 0, 0]

    def add_round(self, other: TeamRoundResult):
        if len(self.rounds) + 1 == other.number:
            self.rounds.append(other)
        elif len(self.rounds) + 1 < other.number:
            for i in range(len(self.rounds) + 1, other.number):
                self.rounds.append(TeamRoundResult(0, 0, 0, False, Position.NONE, i, False))
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

    def __eq__(self, other):
        return self.sum_points() == other.sum_points() and self.sum_speakers() == other.sum_speakers()

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


# TODO @check_tournament
def generate_random_round(tournament: Tournament, cur_round: Round):

    teams = list(tournament.teamtournamentrel_set.filter(role=ROLE_MEMBER))
    chair = list(tournament.usertournamentrel_set.filter(role=ROLE_CHAIR))

    rooms = []
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
        room = Room.objects.create(
            game=game,
            round=cur_round,
            number=i
        )
        rooms.append(room)

    return rooms


def can_show_round(tournament):
    if tournament.status in [STATUS_REGISTRATION, STATUS_PREPARATION] or tournament.cur_round == 0:
        return [False, 'Турнир ещё не начался']

    if tournament.status == STATUS_FINISHED:
        return [False, 'Турнир уже закончился']

    else:
        return [True, '']


def get_current_round_games(tournament: Tournament):
    last_round = Round.objects.filter(
        tournament=tournament,
        is_playoff=(tournament.status == STATUS_PLAYOFF)
    ).latest('number')

    if not last_round:
        return None

    return {
        'games': list(map(lambda x: x.game, Room.objects.filter(round=last_round))),
        'round': last_round,
    }


def get_or_generate_next_round(tournament: Tournament):
    cur_round = Round.objects.filter(
        tournament=tournament,
        is_playoff=(tournament.status == STATUS_PLAYOFF)
    ).latest('number')

    if not cur_round:
        return None
    rooms = Room.objects.filter(round=cur_round)
    if not rooms:
        if tournament.status == STATUS_PLAYOFF:
            rooms = generate_playoff_round(tournament, cur_round)
        elif tournament.cur_round == 1:
            rooms = generate_random_round(tournament, cur_round)
        else:
            rooms = generate_round(tournament, cur_round)

    return rooms


def get_last_round_games_and_results(tournament: Tournament):
    last_round = Round.objects.filter(
        tournament=tournament,
        is_playoff=(tournament.status == STATUS_PLAYOFF)
    ).latest('number')
    if not last_round:
        return None
    results = []
    for room in Room.objects.filter(round=last_round):
        try:
            result = GameResult.objects.get(game=room.game)
        except ObjectDoesNotExist:
            result = None

        results.append({
            'game': room.game,
            'result': result
        })
    return results


def remove_last_round(tournament: Tournament):
    last_round = Round.objects.filter(
        tournament=tournament,
        is_playoff=(tournament.status == STATUS_PLAYOFF)
    ).latest('number')
    if not last_round:
        return False
    for room in Room.objects.filter(round=last_round):
        room.game.delete()
    if last_round.is_playoff and last_round.number < 2:
        tournament.set_status(STATUS_STARTED)
    elif not last_round.is_playoff:
        tournament.round_number_dec()

    last_round.delete()
    return True


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
                bool(game['is_closed'])
            )
            team_id = game[position[0]]
            if team_id not in teams.keys():
                teams[team_id] = TeamResult(team_id)

            teams[team_id].add_round(team_result)

    return list(teams.values())


def generate_playoff_position(count: int):
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


def create_playoff(tournament: Tournament, teams: list):
    positions = list(map(lambda x: x - 1, generate_playoff_position(tournament.count_teams_in_break)))
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


def create_next_round(tournament: Tournament, round_obj):
    """
    round_obj - не сохранённый объект из формы
    """
    if tournament.status == STATUS_STARTED:
        round_obj.tournament = tournament
        round_obj.number = tournament.round_number_inc()
        round_obj.save()
        return

    last_playoff_round = Round.objects.filter(tournament=tournament, is_playoff=True).last()

    if not last_playoff_round:
        return 'Что-то не то 2'

    if last_playoff_round.number == -1:
        motion = last_playoff_round.motion
        last_playoff_round.motion = round_obj.motion
        Game.objects.filter(motion=motion).update(motion=round_obj.motion)
        # motion.delete() при удалении темы, на кторую никто не ссылается пропадает рум
        #  TODO разобраться и удалить временную тему

        last_playoff_round.number = 1
        last_playoff_round.save()
        return

    if last_playoff_round.number > 0:
        round_obj.tournament = tournament
        round_obj.number = last_playoff_round.number + 1
        round_obj.is_playoff = True
        round_obj.save()
        return

    return 'Что-то не то'


def generate_playoff_round(tournament: Tournament, cur_round: Round):
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
        return 'Финал уже был'

    teams_id = []
    for room in result_prev_round:
        for position in positions:
            if room[position[1]] in [1, 2]:
                teams_id.append(room[position[0]])

    rooms = []
    for i in range(len(teams_id) // TEAM_IN_GAME):
        game = Game.objects.create(
            og_id=teams_id.pop(),
            oo_id=teams_id.pop(),
            cg_id=teams_id.pop(),
            co_id=teams_id.pop(),
            chair=chair.pop().user,
            date=datetime.datetime.now(),
            motion=cur_round.motion
        )
        rooms.append(Room.objects.create(
            game=game,
            round=cur_round,
            number=i
        ))

    return rooms


def get_tournament_motions(tournament: Tournament):
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


def check_last_round_results(tournament: Tournament):
    last_rounds = Round.objects.filter(
        tournament=tournament,
        is_playoff=(tournament.status == STATUS_PLAYOFF)
    )
    if not last_rounds:
        return None

    last_round = last_rounds.latest('number')

    for room in Room.objects.filter(round=last_round):
        if not GameResult.objects.filter(game=room.game).exists():
            return 'Введите результаты последнего раунда'

    return None


def generate_round(tournament: Tournament, cur_round: Round):

    tab = sorted(get_tab(tournament), reverse=True)

    def get_teams_with_eq_points(need_position):
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

    games = []
    while tab:

        if len(tab) == 4 or tab[3].sum_points() > tab[4].sum_points():
            pool = tab[:4]
            tab = tab[4:]
            positions = list(find_best_position(pool, (0, 1, 2, 3)))
        elif tab[0].sum_points() > tab[4].sum_points():
            i = 3
            while tab[i - 1].sum_points() == tab[4].sum_points():
                i -= 1
            head_pool = tab[:i]
            tab = tab[i:]
            head_positions = find_best_position(head_pool, (0, 1, 2, 3))

            tail_pool, tail_positions = get_teams_with_eq_points({0, 1, 2, 3} - set(head_positions))
            positions = list(head_positions) + tail_positions
            pool = head_pool + tail_pool
        else:
            pool, positions = get_teams_with_eq_points({0, 1, 2, 3})

        games.append({
            'pool': pool,
            'positions': positions
        })

    rooms = []
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
        room = Room.objects.create(
            game=game,
            round=cur_round,
            number=i
        )
        rooms.append(room)

    return rooms


def find_best_position(pool, need_position):
    n = len(pool)
    best_positions = list(range(n))
    best_sum = sum(list(map(lambda x: pool[x].get_position_weight(best_positions[x]), range(n))))

    for positions in itertools.permutations(need_position, n):
        cur_sum = sum(list(map(lambda x: pool[x].get_position_weight(positions[x]), range(n))))
        if cur_sum < best_sum:
            best_sum = cur_sum
            best_positions = positions

    return best_positions


def find_best_team_in_position(teams, need_positions):
    positions_priority = {}
    max_weight = 0

    def a(positions, find_result):
        if not positions:
            find_teams = list(find_result.values())
            for i in range(len(find_teams)):
                for j in range(i + 1, len(find_teams)):
                    if find_teams[i].team.id == find_teams[j].team.id:
                        return 0, []

            cur_sum = 0
            for key, value in find_result.items():
                cur_sum += value.get_position_weight(key)
            return cur_sum, dict(find_result)

        position = positions.pop()
        best_sum = 0
        best_position = []
        for team in positions_priority[position]:
            if team.get_position_weight(position) > max_weight:
                break
            find_result[position] = team
            cur_sum, cur_position = a(set(positions), find_result)
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


def remove_team_from_tournament(tournament: Tournament, team_id):
    try:
        tournament.teamtournamentrel_set.get(team_id=team_id).delete()
    except ObjectDoesNotExist:
        return 'Не удалось удалить команду'

    return 'Команда упешно удалена'


def can_change_team_role(rel: TeamTournamentRel, role: TournamentRole) -> [bool, str]:
    if role not in [ROLE_IN_TAB, ROLE_MEMBER]:
        return [True, '']

    if check_duplicate_role(role, rel, rel.team.speaker_1):
        return [False, '%s уже участвует в турнире в другой команде' % rel.team.speaker_1.name()]

    if check_duplicate_role(role, rel, rel.team.speaker_2):
        return [False, '%s уже участвует в турнире в другой команде' % rel.team.speaker_1.name()]

    return [True, '']


def check_duplicate_role(role: TournamentRole, rel: TeamTournamentRel, user: User) -> [TeamTournamentRel]:
    return TeamTournamentRel.objects.filter(
        ~Q(id=rel.id),
        Q(team__speaker_1=user) | Q(team__speaker_2=user),
        tournament=rel.tournament,
        role=role
    )
