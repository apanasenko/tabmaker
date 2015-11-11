from django import forms
from .models import \
    Game, \
    GameResult


class GameForm(forms.ModelForm):

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


class ResultGameForm(forms.ModelForm):  # TODO добавить проверку результатов

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


class ActivateResultForm(forms.Form):
    check_game = forms.BooleanField(widget=forms.HiddenInput(attrs={'class': 'is_check_game_input'}))

    def init(self, is_admin):
        self.initial['check_game'] = not is_admin

    def is_active(self):
        return self.cleaned_data['check_game']
