__author__ = 'Alexander'

import random
import datetime
from django.core.exceptions import ObjectDoesNotExist
from apps.game.models import\
    Game, \
    GameResult
from apps.team.models import Team
from .consts import *
from .models import \
    Tournament,\
    Round,\
    Room


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
        self.show_all = False
        self.team = Team.objects.get(pk=team_id)
        self.rounds = []

    def add_round(self, other: TeamRoundResult):
        if len(self.rounds) + 1 == other.number:
            self.rounds.append(other)
        elif len(self.rounds) + 1 < other.number:
            for i in range(len(self.rounds) + 1, other.number):
                self.rounds.append(TeamRoundResult(0, 0, 0, False, Position.NONE, i, False))
            self.rounds.append(other)
        elif len(self.rounds) + 1 > other.number:
            self.rounds[other.number - 1] = other

        return self.rounds

    def sum_points(self):
        return sum(list(map(lambda x: x.points * int(self.show_all or not x.is_closed), self.rounds)))

    def sum_speakers(self):
        return sum(list(map(lambda x: (x.speaker_1 + x.speaker_2) * int(self.show_all), self.rounds)))

    def __gt__(self, other):
        return self.sum_points() > other.sum_points() \
            or self.sum_points() == other.sum_points() and self.sum_speakers() > other.sum_speakers()

    def __eq__(self, other):
        return self.sum_points() == other.sum_points() and self.sum_speakers() == other.sum_speakers()

    def __lt__(self, other):
        return self.sum_points() < other.sum_points() \
            or self.sum_points() == other.sum_points() and self.sum_speakers() < other.sum_speakers()

    def __str__(self):
        return "%s points:%s speakers:%s" % (self.team.name, self.sum_points(), self.sum_speakers())

# def get_member_from_tournament(tournament: Tournament):
#     return tournament.teamtournamentrel_set.filter(role=ROLE_MEMBER)
#
#
# def get_adjudicator_from_tournament(tournament: Tournament):
#     return {
#         'chair': tournament.usertournamentrel_set.filter(role=ROLE_CHAIR),
#         'wing': tournament.usertournamentrel_set.filter(role=ROLE_WING),
#     }


def get_last_round(tournament: Tournament):
    try:
        return Round.objects.get(tournament=tournament, number=tournament.cur_round, is_playoff=False)
    except ObjectDoesNotExist:
        return None


# TODO @check_tournament
def generate_random_round(tournament: Tournament, cur_round: Round):

    teams = list(tournament.teamtournamentrel_set.filter(role=ROLE_MEMBER))
    chair = list(tournament.usertournamentrel_set.filter(role=ROLE_CHAIR))
    # wings = tournament.usertournamentrel_set.filter(role=ROLE_WING)

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
        # game.save()
        room = Room.objects.create(
            game=game,
            round=cur_round
        )
        # room.save()
        rooms.append(room)

    return rooms


def get_or_generate_next_round(tournament: Tournament):
    cur_round = get_last_round(tournament)
    if not cur_round:
        return None
    rooms = Room.objects.filter(round=cur_round)
    if not rooms:
        rooms = generate_random_round(tournament, cur_round)
    return rooms


def get_last_round_games_and_results(tournament: Tournament):
    last_round = get_last_round(tournament)
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
    last_round = get_last_round(tournament)
    if not last_round:
        return False
    for room in Room.objects.filter(round=last_round):
        room.game.delete()
    last_round.delete()
    tournament.round_number_dec()
    return True


def get_tab(tournament: Tournament):
    from .db_execute import get_teams_result_list
    positions = [
        ['og_id', 'og', 'pm', 'dpm', 'og_rev', Position.OG],
        ['oo_id', 'oo', 'lo', 'dlo', 'oo_rev', Position.OO],
        ['cg_id', 'cg', 'mg', 'gw', 'cg_rev', Position.CG],
        ['co_id', 'co', 'mo', 'ow', 'co_rev', Position.CO],
    ]
    teams = {}
    for game in get_teams_result_list(tournament.id):
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
            if not team_id in teams.keys():
                teams[team_id] = TeamResult(team_id)

            teams[team_id].add_round(team_result)

    return list(reversed(sorted(list(teams.values()))))
