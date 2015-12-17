from apps.profile.models import User
from django.shortcuts import \
    get_object_or_404, \
    redirect
from allauth.account.models import EmailAddress
from apps.team.models import Team
from apps.tournament.models import \
    Tournament, \
    TournamentRole,\
    TeamTournamentRel,\
    UserTournamentRel

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
