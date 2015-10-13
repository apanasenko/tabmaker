__author__ = 'Alexander'

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


class ResultGameForm(forms.ModelForm):

    class Meta:
        model = GameResult

        fields = '__all__'

        widgets = {
            'og': forms.NumberInput(attrs={'min': 1, 'max': 4}),
            'oo': forms.NumberInput(attrs={'min': 1, 'max': 4}),
            'cg': forms.NumberInput(attrs={'min': 1, 'max': 4}),
            'co': forms.NumberInput(attrs={'min': 1, 'max': 4}),
            'og_rev': forms.CheckboxInput(attrs={'type': 'checkbox', 'class': 'reverse_speakers'}),
            'oo_rev': forms.CheckboxInput(attrs={'type': 'checkbox', 'class': 'reverse_speakers'}),
            'cg_rev': forms.CheckboxInput(attrs={'type': 'checkbox', 'class': 'reverse_speakers'}),
            'co_rev': forms.CheckboxInput(attrs={'type': 'checkbox', 'class': 'reverse_speakers'}),
            'game': forms.HiddenInput(),
            'pm': forms.NumberInput(attrs={'min': '0', 'max': 100}),
            'dpm': forms.NumberInput(attrs={'min': '0', 'max': 100}),
            'lo': forms.NumberInput(attrs={'min': '0', 'max': 100}),
            'dlo': forms.NumberInput(attrs={'min': '0', 'max': 100}),
            'mg': forms.NumberInput(attrs={'min': '0', 'max': 100}),
            'gw': forms.NumberInput(attrs={'min': '0', 'max': 100}),
            'mo': forms.NumberInput(attrs={'min': '0', 'max': 100}),
            'ow': forms.NumberInput(attrs={'min': '0', 'max': 100}),
        }

        labels = {
            'og_rev': 'Спикеры выступали в обратном порядке',
            'oo_rev': 'Спикеры выступали в обратном порядке',
            'cg_rev': 'Спикеры выступали в обратном порядке',
            'co_rev': 'Спикеры выступали в обратном порядке',
        }

#       TODO добавить проверку результатов
