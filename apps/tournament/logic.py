__author__ = 'Alexander'

import random
import datetime
from django.core.exceptions import ObjectDoesNotExist
from apps.game.models import\
    Game, \
    GameResult
from .consts import *
from .models import \
    Tournament,\
    Round,\
    Room


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
        return Round.objects.get(tournament=tournament, number=tournament.cur_round)
    except Tournament.model.DoesNotExist:
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
