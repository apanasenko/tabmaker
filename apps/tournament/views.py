from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.http import Http404
from apps.tournament.forms import TournamentForm
from apps.tournament.models import Tournament


def index(request):
    raise Http404


def new(request):
    if request.method == 'POST':
        tournament_form = TournamentForm(request.POST)
        if tournament_form.is_valid():
            tournament_obj = tournament_form.save(commit=False)
            tournament_obj.count_rounds = 0
            tournament_obj.save()
            return HttpResponseRedirect('/')  # TODO куда перекидывать

    return render(request, 'tournament/new.html', {'form': TournamentForm()})


def show(request, tournament_id):
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    return render(request, 'tournament/show.html', {'tournament': tournament})


def edit(request, tournament_id):
    if request.method == 'POST':
        tournament = get_object_or_404(Tournament, pk=tournament_id)
        tournament_form = TournamentForm(request.POST, instance=tournament)
        if tournament_form.is_valid():
            tournament_form.save()
            return HttpResponseRedirect('/')

    tournament = get_object_or_404(Tournament, pk=tournament_id)
    return render(
        request,
        'tournament/edit.html',
        {
            'form': TournamentForm(instance=tournament),
            'id': tournament.id,
        }
    )
