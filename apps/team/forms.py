from apps.profile.models import User
from django import forms
from .models import Team


class TeamRegistrationForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = [
            'name',
        ]

    speaker_1 = forms.EmailField()
    speaker_2 = forms.EmailField()

    def clean_speaker_1(self):
        speaker_1 = self.cleaned_data['speaker_1']

        if not User.objects.filter(email=speaker_1).count():  # TODO перевести сообщение об ошибки
            raise forms.ValidationError(u'Пользователь с таким email не зарегистрировался на сайте')

        return speaker_1

    def clean(self):
        super(TeamRegistrationForm, self).clean()
        if self.is_valid() and self.cleaned_data['speaker_1'] == self.cleaned_data['speaker_2']:  # TODO перевести сообщение об ошибки
            raise forms.ValidationError(u'Email первого и второго спикера должны различаться')

    def clean_speaker_2(self):
        speaker_2 = self.cleaned_data['speaker_2']

        if not User.objects.filter(email=speaker_2).count():  # TODO перевести сообщение об ошибки
            raise forms.ValidationError(u'Пользователь с таким email не зарегистрировался на сайте')

        return speaker_2

    def save(self, commit=True):
        team = super(TeamRegistrationForm, self).save(commit=False)
        team.speaker_1 = User.objects.get(email=self.cleaned_data['speaker_1'])
        team.speaker_2 = User.objects.get(email=self.cleaned_data['speaker_2'])
        if commit:
            team.save()
        return team


class TeamWithSpeakerRegistrationForm(TeamRegistrationForm):

    def __init__(self, *args, **kwargs):
        super(TeamRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['speaker_1'].widget = forms.HiddenInput()

    def save(self, speaker_1=None, commit=True):
        team = super(TeamWithSpeakerRegistrationForm, self).save(commit=False)
        team.speaker_1 = speaker_1
        team.speaker_2 = User.objects.get(email=self.cleaned_data['speaker_2'])
        if commit:
            team.save()
        return team
