__author__ = 'Alexander'

import pytz

from django import forms
from datetime import datetime
from . models import \
    Tournament, \
    TeamTournamentRel, \
    Round


class TournamentForm(forms.ModelForm):

    open_reg_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'datepicker', 'type': 'date'}), label=u'Дата открытия регистрации')
    open_reg_time = forms.TimeField(
        widget=forms.DateInput(attrs={'class': 'timepicker', 'type': 'time'}), label=u'Время открытия регистрации')

    close_reg_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'datepicker', 'type': 'date'}), label=u'Дата закрытия регистрации')
    close_reg_time = forms.TimeField(
        widget=forms.DateInput(attrs={'class': 'timepicker', 'type': 'time'}), label=u'Время закрытия регистрации')

    start_tour_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'datepicker', 'type': 'date'}), label=u'Дата закрытия регистрации')
    start_tour_time = forms.TimeField(
        widget=forms.DateInput(attrs={'class': 'timepicker', 'type': 'time'}), label=u'Время закрытия регистрации')

    class Meta:
        model = Tournament
        fields = [
            'name',
            'location',
            'info',
            'count_rounds',
            'count_teams',
            'count_teams_in_break',
            'link',
        ]

        widgets = {
            'name': forms.TextInput(attrs={'class': 'validate'}),
            'location': forms.TextInput(attrs={'class': 'validate'}),
            'count_rounds': forms.NumberInput(attrs={'min': '0'}),
            'count_teams': forms.NumberInput(attrs={'min': '0', 'step': 4}),
            'count_teams_in_break': forms.NumberInput(attrs={'min': '0', 'step': 4}),
            'link': forms.URLInput(attrs={'class': 'validate'}),
            'info': forms.Textarea(attrs={'class': 'materialize-textarea'}),
        }

        labels = {
            'name': 'Название турнира',
            'location': 'Место проведения',
            'count_rounds': 'Количество раундов',
            'count_teams': 'Количество команд',
            'count_teams_in_break': 'Команд break\'е',
            'link': 'Ссылка на соц.сеть',
            'info': 'О турнире',
        }

    # def clean_close_reg_date(self):
    #     open_reg_date = self.cleaned_data['open_reg_date']
    #     close_reg_date = self.cleaned_data['close_reg_date']
    #
    #     if open_reg_date > close_reg_date:
    #         raise forms.ValidationError(u'Регистрация заканчивается раньше, чем открывается')
    #
    #     return close_reg_date
    #
    # def clean_start_tour_date(self):
    #     close_reg_date = self.cleaned_data['close_reg_date']
    #     start_tour_date = self.cleaned_data['start_tour_date']
    #
    #     if start_tour_date < close_reg_date:
    #         raise forms.ValidationError(u'Турнир начинается раньше, чем закрывается регистрация')
    #
    #     return close_reg_date

    def __init__(self, *args, **kwargs):
        super(TournamentForm, self).__init__(*args, **kwargs)
        if self.instance.open_reg:
            self.initial['open_reg_date'] = self.instance.open_reg.date().isoformat()
            self.initial['open_reg_time'] = self.instance.open_reg.time().isoformat()
        if self.instance.close_reg:
            self.initial['close_reg_date'] = self.instance.close_reg.date().isoformat()
            self.initial['close_reg_time'] = self.instance.close_reg.time().isoformat()
        if self.instance.start_tour:
            self.initial['start_tour_date'] = self.instance.start_tour.date().isoformat()
            self.initial['start_tour_time'] = self.instance.start_tour.time().isoformat()

    def save(self, commit=True):
        tournament = super(TournamentForm, self).save(False)
        tournament.open_reg = datetime.combine(
            self.cleaned_data['open_reg_date'],
            self.cleaned_data['open_reg_time'].replace(tzinfo=pytz.utc)
        )
        tournament.close_reg = datetime.combine(
            self.cleaned_data['close_reg_date'],
            self.cleaned_data['close_reg_time'].replace(tzinfo=pytz.utc)
        )
        tournament.start_tour = datetime.combine(
            self.cleaned_data['start_tour_date'],
            self.cleaned_data['start_tour_time'].replace(tzinfo=pytz.utc)
        )
        if commit:
            tournament.save()
        return tournament


class TeamRoleForm(forms.ModelForm):
    class Meta:
        model = TeamTournamentRel
        fields = [
            'role'
        ]
#       TODO Добавить фильтр ролей и перевод


class AdjudicatorRoleForm(forms.ModelForm):
    class Meta:
        model = TeamTournamentRel
        fields = [
            'role'
        ]


class RoundForm(forms.ModelForm):

    start_round_time = forms.TimeField(
        widget=forms.DateInput(attrs={'class': 'timepicker', 'type': 'time'}), label=u'Время начала раунда')

    class Meta:
        model = Round
        fields = [
            'is_closed'
        ]

        labels = {
            'is_closed': 'Закрытый раунд'
        }

        widgets = {
            'is_closed': forms.CheckboxInput(attrs={'type': 'checkbox'})
        }

    def save(self, commit=True):
        round_obj = super(RoundForm, self).save(False)
        round_obj.start_time = datetime.combine(
            datetime.now().date(),
            self.cleaned_data['start_round_time'].replace(tzinfo=pytz.utc)
        )
        if commit:
            round_obj.save()
        return round_obj


class CheckboxForm(forms.Form):
    is_check = forms.BooleanField()
    id = forms.IntegerField(widget=forms.HiddenInput())
