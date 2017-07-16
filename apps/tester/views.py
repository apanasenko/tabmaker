from django.shortcuts import \
    get_object_or_404, \
    redirect
from allauth.account.models import EmailAddress
from apps.tournament.models import \
    Tournament, \
    TournamentRole,\
    TeamTournamentRel,\
    UserTournamentRel,\
    Team, \
    User

import random


def generate_user(name_length=5):
    letters = list(map(chr, range(ord('a'), ord('z') + 1)))

    name = 'user_'
    while name == 'user_':
        for i in range(name_length):
            name += random.choice(letters)
        if len(User.objects.filter(username=name)):
            name_length += 1
            name = 'user_'

    password = '1'
    email = name + '@test.test'
    u = User.objects.create_user(username=name, email=email, password=password)
    u.save()
    e = EmailAddress.objects.create(user=u, email=u.email, verified=True, primary=True)
    e.save()

    return u


def generate_team(name_length=5):
    letters = list(map(chr, range(ord('a'), ord('z') + 1)))

    name = 'test_team_'
    while name == 'test_team_':
        for i in range(name_length):
            name += random.choice(letters)
        # print(name_length, name, Team.objects.filter(name=name))
        if len(Team.objects.filter(name=name)):
            name_length += 1
            name = 'test_team_'

    t = Team.objects.create(
        name=name,
        speaker_1=generate_user(10),
        speaker_2=generate_user(10),
        info='Test Team'
    )
    t.save()

    return t


def add_team_to_tournament(tournament: Tournament, count_team: int, role: TournamentRole):
    for i in range(count_team):
        TeamTournamentRel.objects.create(
            team=generate_team(),
            tournament=tournament,
            role=role
        )


def add_user_to_tournament(tournament: Tournament, count_adjudicator: int, role: TournamentRole):
    for i in range(count_adjudicator):
        UserTournamentRel.objects.create(
            user=generate_user(),
            tournament=tournament,
            role=role
        )


def generate(request, tournament_id: int, func: str, role_id: int, count: int):
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    role = get_object_or_404(TournamentRole, pk=role_id)
    generate_func = add_team_to_tournament if func == 'team' else add_user_to_tournament
    generate_func(tournament, int(count), role)
    return redirect('/tournament/%s/%s/list/' % (tournament_id, func))


def generate_places(request, tournament_id: int, count: int):
    from apps.tournament.models import Place

    tournament = get_object_or_404(Tournament, pk=tournament_id)
    for i in range(int(count)):
        number = '%d' % random.randint(10000, 100000)
        Place.objects.get_or_create(tournament=tournament, place=number)
    return redirect('/tournament/%s/place/edit/' % tournament_id)


def generate_results(request, tournament_id: int, rev=30, exist=5):
    """
    rev in [0, 100]
    exist in [0, 100]
    """
    from apps.tournament.logic import get_rooms_from_last_round
    from apps.tournament.models import QualificationResult

    tournament = get_object_or_404(Tournament, pk=tournament_id)
    rooms = get_rooms_from_last_round(tournament)
    for room in rooms:
        result = {}
        places = [1, 2, 3, 4]
        random.shuffle(places)
        speakers = sorted([random.randrange(51, 99) for _ in range(8)], reverse=True)
        positions = [
            ['og', 'pm', 'dpm'],
            ['oo', 'lo', 'dlo'],
            ['cg', 'mg', 'gw'],
            ['co', 'mo', 'ow'],
        ]
        for i in positions:
            # Team point
            p = places.pop()
            result[i[0]] = p
            # Speakers
            x = random.randint(1, 2)
            result[i[x]] = speakers[(p - 1) * 2]
            result[i[3 - x]] = speakers[(p - 1) * 2 + 1]
            # Is revert speakers
            if random.randint(0, 100) < rev:
                result[i[0] + '_rev'] = True
            # Is exist speakers 1
            if random.randint(0, 100) < exist:
                result[i[1] + '_exist'] = False
                result[i[1]] = 0
            # Is exist speakers 2
            if random.randint(0, 100) < exist:
                result[i[2] + '_exist'] = False
                result[i[2]] = 0

        QualificationResult.objects.update_or_create(defaults=result, game=room.game)

    return redirect('/tournament/%s/round/result/' % tournament_id)


def remove(request, actor: str, id: int):
    if actor == 'user':
        user = get_object_or_404(User, pk=id)
        user.delete()

    return redirect('main:index')


def clone_tournament(request, count: int):
    tournaments = list()
    for i in range(int(count)):
        t = Tournament.objects.all().order_by('?').first()
        t.pk = None
        t.name += '_%s' % i
        t.name = t.name[:100]
        t.save()

    return redirect('main:index')


def restart_tournament(request, tournament_id: int):
    from apps.tournament.consts import STATUS_PLAYOFF, ROLE_OWNER

    tournament = get_object_or_404(Tournament, pk=tournament_id)
    tournament.status = STATUS_PLAYOFF
    tournament.save()
    if request.user.is_authenticated():
        rel = UserTournamentRel.objects.get(tournament=tournament, role=ROLE_OWNER)
        rel.user = request.user
        rel.save()

    return redirect('tournament:show', tournament_id=tournament.id)
