from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from apps.team.forms import TeamRegistrationForm
from apps.tournament.forms import TournamentForm
from apps.tournament.models import Tournament
from apps.tournament.models import TournamentRole
from apps.tournament.models import TeamTournamentRel
from apps.tournament.models import UserTournamentRel


def index(request):
    # TODO придумать зачем эта страница
    return show_message(request, 'Нужна ди эта страница?')


@login_required
def new(request):
    if request.method == 'POST':
        tournament_form = TournamentForm(request.POST)
        if tournament_form.is_valid():
            tournament_obj = tournament_form.save(commit=False)
            tournament_obj.count_rounds = 0
            tournament_obj.save()
            UserTournamentRel.objects.create(
                user=request.user,
                tournament=tournament_obj,
                role=TournamentRole.objects.get(role='owner'),
            )

            # TODO куда перекидывать
            return show_message(request, 'Вы создали свой турнир')

    else:
        tournament_form = TournamentForm()

    return render(request, 'tournament/new.html', {'form': tournament_form})


def show(request, tournament_id):
    tournament = get_object_or_404(Tournament, pk=tournament_id)

    return render(
        request,
        'tournament/show.html',
        {
            'tournament': tournament,
            'is_owner': user_can_edit_tournament(tournament, request.user)
        }
    )


@login_required
def edit(request, tournament_id):
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    if not user_can_edit_tournament(tournament, request.user):
        # TODO страница ошибки доступа
        return show_message(request, 'У вас нет прав для редактирования турнира')

    if request.method == 'POST':
        tournament_form = TournamentForm(request.POST, instance=tournament)
        if tournament_form.is_valid():
            tournament_form.save()

            return show_message(request, 'Турнир изменён')

    else:
        tournament_form = TournamentForm(instance=tournament)

    return render(
        request,
        'tournament/edit.html',
        {
            'form': tournament_form,
            'id': tournament.id,
        }
    )


@login_required
def registration(request, tournament_id):
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    if request.method == 'POST':
        team_form = TeamRegistrationForm(request.POST)
        if team_form.is_valid():
            team_obj = team_form.save(commit=False)
            team_obj.speaker_1 = request.user
            team_obj.speaker_2 = User.objects.get(email=team_form.cleaned_data['speaker_2'])
            team_obj.save()
            TeamTournamentRel.objects.create(
                team=team_obj,
                tournament=tournament,
                role=TournamentRole.objects.get(role='registered'),
            )

            return show_message(request, 'Вы успешно зарегались в %s' % tournament.name)

    else:
        team_form = TeamRegistrationForm(initial={'speaker_1': request.user.email})

    return render(
        request,
        'tournament/registration.html',
        {
            'form': team_form,
            'id': tournament_id,
            'user': request.user,
        }
    )


def user_can_edit_tournament(t: Tournament, u: User):
    # TODO добавить админов
    return u.is_authenticated() and 0 < len(UserTournamentRel.objects.filter(
        tournament=t,
        user=u,
        role=TournamentRole.objects.get(role='owner')
    ))


def show_message(request, message):
    return render(request, 'main/message.html', {'message': message})
