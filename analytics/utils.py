from apps.tournament.models import Team, User, Game


def og_res_collector(user: User, team: Team):
    first_speaker = team.speaker_1 == user

    def game_proc(game: Game):
        try:
            res = game.gameresult
            g_res = game.gameresult.qualificationresult
        except:
            return
        if not res.og_rev:
            return g_res.og, g_res.pm if first_speaker else g_res.og, g_res.dpm
        else:
            return g_res.og, g_res.dpm if first_speaker else g_res.og, g_res.pm
    return game_proc


def oo_res_collector(user: User, team: Team):
    first_speaker = team.speaker_1 == user

    def game_proc(game: Game):
        try:
            res = game.gameresult
            g_res = game.gameresult.qualificationresult
        except:
            return
        if not res.oo_rev:
            return g_res.oo, g_res.lo if first_speaker else g_res.oo, g_res.dlo
        else:
            return g_res.oo, g_res.dlo if first_speaker else g_res.oo, g_res.lo
    return game_proc


def cg_res_collector(user: User, team: Team):
    first_speaker = team.speaker_1 == user

    def game_proc(game: Game):
        try:
            res = game.gameresult
            g_res = game.gameresult.qualificationresult
        except:
            return
        if not res.cg_rev:
            return g_res.cg, g_res.mg if first_speaker else g_res.cg, g_res.gw
        else:
            return g_res.cg, g_res.gw if first_speaker else g_res.cg, g_res.mg

    return game_proc

def co_res_collector(user: User, team: Team):
    first_speaker = team.speaker_1 == user

    def game_proc(game: Game):
        try:
            res = game.gameresult
            g_res = game.gameresult.qualificationresult
        except:
            return
        if not res.oo_rev:
            return g_res.co, g_res.mo if first_speaker else g_res.co, g_res.ow
        else:
            return g_res.co, g_res.ow if first_speaker else g_res.co, g_res.mo
    return game_proc
