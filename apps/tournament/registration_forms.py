from django import forms
from apps.profile.models import User
from apps.team.models import Team
from apps.tournament.consts import \
    FIELD_ALIAS_TEAM, \
    FIELD_ALIAS_SPEAKER_1, \
    FIELD_ALIAS_SPEAKER_2


class TeamRegistrationForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = [
            'name',
        ]
        labels = {
            'name': 'Название команды',
        }

    speaker_1 = forms.EmailField(label='E-mail первого спикера')
    speaker_2 = forms.EmailField(label='E-mail второго спикера')

    _required_fields = {
        FIELD_ALIAS_TEAM.name: 'name',
        FIELD_ALIAS_SPEAKER_1.name: 'speaker_1',
        FIELD_ALIAS_SPEAKER_2.name: 'speaker_2',
    }

    def clean_speaker_1(self):
        speaker_1 = self.cleaned_data['speaker_1']

        if not User.objects.filter(email=speaker_1).count():
            raise forms.ValidationError(u'Пользователь с таким email не зарегистрировался на сайте')

        return speaker_1

    def clean_speaker_2(self):
        speaker_2 = self.cleaned_data['speaker_2']

        if not User.objects.filter(email=speaker_2).count():
            raise forms.ValidationError(u'Пользователь с таким email не зарегистрировался на сайте')

        return speaker_2

    def clean(self):
        super(TeamRegistrationForm, self).clean()
        if self.is_valid() and self.cleaned_data['speaker_1'] == self.cleaned_data['speaker_2']:
            raise forms.ValidationError(u'Email первого и второго спикера должны различаться')

    def save(self, commit=True):
        team = super(TeamRegistrationForm, self).save(commit=False)
        team.speaker_1 = User.objects.get(email=self.cleaned_data['speaker_1'])
        team.speaker_2 = User.objects.get(email=self.cleaned_data['speaker_2'])
        if commit:
            team.save()
        return team


class TeamWithSpeakerRegistrationForm(TeamRegistrationForm):

    def __init__(self, questions=None, *args, **kwargs):
        # :questions: - Для единого интерфейса с CustomTeamRegistrationForm
        super(TeamRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['speaker_1'].widget.attrs['readonly'] = True
        self.fields['speaker_1'].label = 'Ваш e-mail'
        self.fields['speaker_2'].label = 'E-mail вашего напарника'

    def save(self, speaker_1=None, commit=True):
        team = super(TeamWithSpeakerRegistrationForm, self).save(commit=False)
        team.speaker_1 = speaker_1
        if commit:
            team.save()
        return team


class CustomTeamRegistrationForm(TeamWithSpeakerRegistrationForm):

    required_css_class = 'required'

    def __init__(self, questions, *args, **kwargs):
        super(CustomTeamRegistrationForm, self).__init__(questions, *args, **kwargs)
        self.fields.keyOrder = []
        for question in questions:
            if question.alias and question.alias.name in self._required_fields:
                field_name = self._required_fields[question.alias.name]
                self.fields[field_name].label = question.question
                self.fields[field_name].help_text = question.comment
                self.fields[field_name].required = question.required
            else:
                field_name = 'question_%s' % question.position
                self.fields[field_name] = forms.CharField(
                    label=question.question,
                    help_text=question.comment,
                    required=question.required,
                )
            self.fields.keyOrder.append(field_name)

    def save(self, speaker_1=None, commit=True):
        team = super(CustomTeamRegistrationForm, self).save(speaker_1, False)
        if commit:
            team.save()
        return team
