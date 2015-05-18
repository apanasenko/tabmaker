__author__ = 'Alexander'

from apps.profile.models import User
from django import forms
from .models import Team


class TeamRegistrationForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = [
            'name',
            'info'
        ]

    speaker_1 = forms.EmailField(widget=forms.HiddenInput)
    speaker_2 = forms.EmailField()

    def clean_speaker_2(self):
        speaker_1 = self.cleaned_data['speaker_1']
        speaker_2 = self.cleaned_data['speaker_2']

        if speaker_1 == speaker_2:  # TODO перевести сообщение об ошибки
            raise forms.ValidationError(u'Ваш email и email вашего тимейта должны различаться')

        if not len(User.objects.filter(email=speaker_2)):  # TODO перевести сообщение об ошибки
            raise forms.ValidationError(u'Пользователя с таким email не существует')

        return speaker_2
