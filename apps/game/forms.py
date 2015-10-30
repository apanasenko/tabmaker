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
        speaker_1_attrs = {'min': '50', 'max': 100, 'class': 'speaker_1_points'}
        speaker_2_attrs = {'min': '50', 'max': 100, 'class': 'speaker_2_points'}
        team_attrs = {'min': 1, 'max': 4, 'class': 'place'}
        reverse_checkbox_attrs = {'type': 'checkbox', 'class': 'reverse_speakers'}

        fields = '__all__'

        widgets = {
            'og': forms.NumberInput(attrs=team_attrs),
            'oo': forms.NumberInput(attrs=team_attrs),
            'cg': forms.NumberInput(attrs=team_attrs),
            'co': forms.NumberInput(attrs=team_attrs),
            'og_rev': forms.CheckboxInput(attrs=reverse_checkbox_attrs),
            'oo_rev': forms.CheckboxInput(attrs=reverse_checkbox_attrs),
            'cg_rev': forms.CheckboxInput(attrs=reverse_checkbox_attrs),
            'co_rev': forms.CheckboxInput(attrs=reverse_checkbox_attrs),
            'game': forms.HiddenInput(),
            'pm': forms.NumberInput(attrs=speaker_1_attrs),
            'dpm': forms.NumberInput(attrs=speaker_2_attrs),
            'lo': forms.NumberInput(attrs=speaker_1_attrs),
            'dlo': forms.NumberInput(attrs=speaker_2_attrs),
            'mg': forms.NumberInput(attrs=speaker_1_attrs),
            'gw': forms.NumberInput(attrs=speaker_2_attrs),
            'mo': forms.NumberInput(attrs=speaker_1_attrs),
            'ow': forms.NumberInput(attrs=speaker_2_attrs),
        }

        labels = {
            'og_rev': 'Спикеры выступали в обратном порядке',
            'oo_rev': 'Спикеры выступали в обратном порядке',
            'cg_rev': 'Спикеры выступали в обратном порядке',
            'co_rev': 'Спикеры выступали в обратном порядке',
        }

#       TODO добавить проверку результатов
