import pytz

from django import forms
from datetime import datetime
from . models import \
    Tournament, \
    Round


class TournamentForm(forms.ModelForm):

    open_reg_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'datepicker tournament-new__date', 'type': 'date', 'placeholder': 'Дата'}), label=u'Дата открытия регистрации')
    open_reg_time = forms.TimeField(
        widget=forms.DateInput(attrs={'class': 'timepicker tournament-new__time', 'type': 'time', 'placeholder': 'Время'}), label=u'Время открытия регистрации')

    close_reg_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'datepicker tournament-new__date', 'type': 'date', 'placeholder': 'Дата'}), label=u'Дата закрытия регистрации')
    close_reg_time = forms.TimeField(
        widget=forms.DateInput(attrs={'class': 'timepicker tournament-new__time', 'type': 'time', 'placeholder': 'Время'}), label=u'Время закрытия регистрации')

    start_tour_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'datepicker tournament-new__date', 'type': 'date', 'placeholder': 'Дата'}), label=u'Дата начала турнира')
    start_tour_time = forms.TimeField(
        widget=forms.DateInput(attrs={'class': 'timepicker tournament-new__time', 'type': 'time', 'placeholder': 'Время'}), label=u'Время начала турнира')

    class Meta:
        model = Tournament
        fields = [
            'name',
            'location',
            'location_lon',
            'location_lat',
            'info',
            'count_rounds',
            'count_teams',
            'count_teams_in_break',
            'link',
        ]

        widgets = {
            'name': forms.TextInput(attrs={'class': 'validate', 'placeholder': 'Название'}),
            'location': forms.TextInput(attrs={
                'class': 'validate',
                'placeholder': 'Укажите место на карте',
                'readonly': 'True',
            }),
            'location_lon': forms.HiddenInput(),
            'location_lat': forms.HiddenInput(),
            'count_rounds': forms.NumberInput(attrs={'min': '0', 'placeholder': 'Количество отборочных', 'class': 'tournament-new__count'}),
            'count_teams': forms.NumberInput(attrs={'min': '0', 'step': 4, 'placeholder': 'Максимум команд', 'class': 'tournament-new__count'}),
            'count_teams_in_break': forms.NumberInput(attrs={'min': '0', 'step': 4, 'placeholder': 'Выходят в плей-офф', 'class': 'tournament-new__count'}),
            'link': forms.URLInput(attrs={'class': 'validate', 'placeholder': 'Cсылка в социальных сетях'}),
            'info': forms.Textarea(attrs={'placeholder': 'О турнире', 'rows': '5'}),
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


class СonfirmForm(forms.Form):
    message = forms.CharField(widget=forms.TextInput())


########################################################################################
# game.forms
########################################################################################

from .models import \
    Game, \
    GameResult


class GameForm(forms.ModelForm):
    place_id = forms.IntegerField(widget=forms.HiddenInput(attrs={'class': 'place_id'}))
    place_name = ''

    class Meta:
        model = Game
        fields = [
            'og',
            'oo',
            'cg',
            'co',
            'chair',
        ]

        widgets = {
            'og': forms.HiddenInput(attrs={'class': 'team_id'}),
            'oo': forms.HiddenInput(attrs={'class': 'team_id'}),
            'cg': forms.HiddenInput(attrs={'class': 'team_id'}),
            'co': forms.HiddenInput(attrs={'class': 'team_id'}),
            'chair': forms.HiddenInput(attrs={'class': 'chair_id'}),
        }

    def init_place(self, place):
        self.initial['place_id'] = place.id
        self.place_name = place.place

    def get_place_id(self):
        return self.cleaned_data['place_id']

    def save(self, commit=True):
        game = super(GameForm, self).save(commit)
        if len(self.changed_data) > 1 or len(self.changed_data) == 1 and self.changed_data[0] != 'place_id':
            GameResult.objects.filter(game=game).delete()

        return game


class ResultGameForm(forms.ModelForm):

    min_speaker_points = 50

    class Meta:
        model = GameResult

        fields = '__all__'

        labels = {}
        widgets = {
            'game': forms.HiddenInput(attrs={'class': 'game_id'}),
        }

        for i in ['og', 'oo', 'cg', 'co']:
            widgets[i] = forms.NumberInput(attrs={'min': 1, 'max': 4, 'class': 'place'})

        for i in ['og_rev', 'oo_rev', 'cg_rev', 'co_rev']:
            widgets[i] = forms.CheckboxInput(attrs={'type': 'checkbox', 'class': 'reverse_speakers'})
            labels[i] = 'Спикеры выступали в обратном порядке'

        for i in ['pm', 'lo', 'mg', 'mo']:
            widgets[i] = forms.NumberInput(attrs={'min': 0, 'max': 100, 'class': 'speaker_1_points points_input'})

        for i in ['dpm', 'dlo', 'gw', 'ow']:
            widgets[i] = forms.NumberInput(attrs={'min': 0, 'max': 100, 'class': 'speaker_2_points points_input'})

        for i in ['pm_exist', 'lo_exist', 'mg_exist', 'mo_exist', 'dpm_exist', 'dlo_exist', 'gw_exist', 'ow_exist']:
            widgets[i] = forms.CheckboxInput(attrs={'type': 'checkbox', 'class': 'exist_speaker'})

    def clean(self):
        super(ResultGameForm, self).clean()
        if not self.is_valid():
            return

        for i in ['pm', 'lo', 'mg', 'mo', 'dpm', 'dlo', 'gw', 'ow']:
            if self.cleaned_data[i + '_exist']:
                if self.cleaned_data[i] < self.min_speaker_points:
                    self.add_error(i, 'Спикерский балл не должен быть меньше %s' % self.min_speaker_points)

            else:
                self.cleaned_data[i] = 0

        places = sorted(list(map(lambda x: self.cleaned_data[x], ['og', 'oo', 'cg', 'co'])))
        a = [1, 2, 3, 4]
        if places != a:
            for i in a:
                if i not in places:
                    self.add_error('__all__', 'Не указана команда, занявшая %s место' % i)


class ActivateResultForm(forms.Form):
    check_game = forms.BooleanField(widget=forms.HiddenInput(attrs={'class': 'is_check_game_input'}))

    def init(self, is_admin):
        self.initial['check_game'] = not is_admin

    def is_active(self):
        return self.cleaned_data['check_game']


#######################################################################################################
# motion
#######################################################################################################

from .models import Motion


class MotionForm(forms.ModelForm):
    class Meta:
        model = Motion

        fields = [
            'motion',
            'infoslide',
        ]

        labels = {
            'motion': 'Резолюция',
            'infoslide': 'Инфослайд',
        }

        widgets = {
            'motion': forms.Textarea(attrs={'class': 'materialize-textarea'}),
            'infoslide': forms.Textarea(attrs={'class': 'materialize-textarea'}),
        }
