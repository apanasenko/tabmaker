__author__ = 'Alexander'

from django.forms import ModelForm
from django.contrib.admin import widgets
from .models import Tournament


class TournamentForm(ModelForm):
    class Meta:
        model = Tournament
        fields = [
            'name',
            'location',
            'info',
            'open_reg',
            'close_reg',
            'start_tour',
        ]
        widgets = {
            'open_reg': widgets.AdminSplitDateTime(),
            'close_reg': widgets.AdminSplitDateTime(),
            'start_tour': widgets.AdminSplitDateTime(),
        }
