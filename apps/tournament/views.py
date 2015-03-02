from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.http import Http404
from apps.tournament.forms import TournamentForm
from apps.tournament.models import Tournament


def index(request):
    # TODO придумать зачем эта страница
    return show_message(request, 'Нужна ди эта страница?')


def new(request):
    if request.method == 'POST':
        tournament_form = TournamentForm(request.POST)
        if tournament_form.is_valid():
            tournament_obj = tournament_form.save(commit=False)
            tournament_obj.count_rounds = 0
            tournament_obj.save()
            # TODO куда перекидывать
            return show_message(request, 'Вы создали свой турнир')

    return render(request, 'tournament/new.html', {'form': TournamentForm()})


def show(request, tournament_id):
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    return render(request, 'tournament/show.html', {'tournament': tournament})


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

    return render(
        request,
        'tournament/edit.html',
        {
            'form': TournamentForm(instance=tournament),
            'id': tournament.id,
        }
    )
def show_message(request, message):
    return render(request, 'main/message.html', {'message': message})
