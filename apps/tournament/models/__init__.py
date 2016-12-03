#########################
#
# TODO Сделать диаграмму связей
# Models dependence:
#   profile
#   motion
#   team -> profile
#   game -> team, profile, motion
#   tournament -> team, profile
#   place -> tournament
#   round -> tournament, motion
#   room -> round, place, game
#   page -> tournament
#   custom_form  -> tournament
#
#########################

from . profile import \
    City, \
    Country, \
    University, \
    User

from . motion import Motion
from . team import Team
from . game import \
    Game, \
    GameResult, \
    PlayoffResult, \
    QualificationResult

from . tournament import \
    TeamTournamentRel, \
    Tournament, \
    TournamentRole, \
    TournamentStatus, \
    UserTournamentRel

from . place import Place
from . round import Round
from . room import Room
from . page import \
    AccessToPage, \
    Page

from .custom_form import \
    CustomForm, \
    CustomFieldAlias, \
    CustomFormAnswers, \
    CustomFormType, \
    CustomQuestion