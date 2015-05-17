__author__ = 'Alexander'

from django import forms
from .models import Game


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

