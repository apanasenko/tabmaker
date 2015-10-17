import json
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_protect
from apps.team.models import Team
from apps.tournament.models import UserTournamentRel
from apps.tournament.consts import STATUS_REGISTRATION


def json_response(status: str, message: str):
    return HttpResponse(
        json.dumps({
            'status': status,
            "message": message,
        }),
        content_type="application/json"
    )


def can_remove_team(team: Team) -> bool:
    result = True
    for tournament in team.tournament_set.all():
        result &= tournament.status == STATUS_REGISTRATION

    return result


def can_remove_adjudicator(rel: UserTournamentRel) -> bool:
    return rel.tournament.status == STATUS_REGISTRATION


@csrf_protect
@login_required(login_url=reverse_lazy('account_login'))
def team_remove(request):
    if request.method != 'POST' or not request.is_ajax():
        return HttpResponseBadRequest

    team = get_object_or_404(Team, pk=request.POST.get('team_id', '0'))
    if not team:
        return json_response('bad', 'Такой команды не существует')

    if request.user != team.speaker_1 and request.user != team.speaker_2:
        return json_response('bad', 'Вы не являетесь членом этой команды')

    if not can_remove_team(team):
        return json_response('bad', 'Команда уже участвует в турнире')

    team.delete()

    return json_response('ok', 'Команда успешно удалена')


@csrf_protect
@login_required(login_url=reverse_lazy('account_login'))
def adjudicator_remove(request):
    if request.method != 'POST' or not request.is_ajax():
        return HttpResponseBadRequest

    user_tournament_rel = get_object_or_404(UserTournamentRel, pk=request.POST.get('user_tournament_rel_id', '0'))
    if not user_tournament_rel:
        return json_response('bad', 'Такой заявки не существует')

    if request.user != user_tournament_rel.user:
        return json_response('bad', 'Невозможно удалить чужую заявку')

    if not can_remove_adjudicator(user_tournament_rel):
        return json_response('bad', 'Турнир уже начался')

    user_tournament_rel.delete()

    return json_response('ok', 'Заявка успешно удалена')
