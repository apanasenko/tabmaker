from django.db import connection


def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


def get_teams_result_list(where, params):
    # TODO Может быть возможно убрать названия таблиц и брать их из моделей Model._meta.db_table
    # пока как параметр вставить не получилось

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT
                round.number,
                round.is_closed,
                game.og_id,
                game.oo_id,
                game.cg_id,
                game.co_id,
                result.*
            FROM tournament_round as round
            INNER JOIN tournament_room as room ON round.id = room.round_id
            INNER JOIN game_game as game ON room.game_id = game.id
            INNER JOIN game_gameresult as result ON result.game_id = game.id
            """ + where,
            params
        )
        return dictfetchall(cursor)


def get_motion_list(tournament_id):

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT
                round.number,
                round.is_playoff,
                motion.motion,
                motion.infoslide,
                count(room.id)
            FROM tournament_round AS round
            INNER JOIN motion_motion AS motion ON round.motion_id = motion.id
            INNER JOIN tournament_room AS room ON room.round_id = round.id
            WHERE
                tournament_id = %s
            GROUP BY
                round.id,
                motion.motion,
                motion.infoslide
            ORDER BY
                round.is_playoff,
                round.number
            """,
            [tournament_id]
        )
        return dictfetchall(cursor)
