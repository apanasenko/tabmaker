__author__ = 'Alexander'

from django import forms
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
