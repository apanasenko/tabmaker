from django.shortcuts import render
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress
from apps.team.models import Team
from apps.tournament.models import Tournament
from apps.tournament.models import TournamentRole
from apps.tournament.models import TeamTournamentRel

import random


def generate_user(name_length=5):
    letters = list(map(chr, range(ord('a'), ord('z') + 1)))

    name = ''
    while name == '':
        for i in range(name_length):
            name += random.choice(letters)
        if len(User.objects.filter(username=name)):
            name_length += 1
            name = ''

    password = '1'
    email = name + '@aaa.aaa'
    u = User.objects.create_user(username=name, email=email, password=password)
    u.save()
    e = EmailAddress.objects.create(user=u, email=u.email, verified=True, primary=True)
    e.save()

    return u


def generate_team(name_length=5):
    letters = list(map(chr, range(ord('a'), ord('z') + 1)))

    name = ''
    while name == '':
        for i in range(name_length):
            name += random.choice(letters)
        print(name_length, name, Team.objects.filter(name=name))
        if len(Team.objects.filter(name=name)):
            name_length += 1
            name = ''

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