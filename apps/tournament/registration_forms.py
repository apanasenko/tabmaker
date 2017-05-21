from collections import OrderedDict

from django import forms
from apps.tournament.models import Team, Tournament, User
from apps.tournament.consts import \
    FIELD_ALIAS_ADJUDICATOR, \
    FIELD_ALIAS_SPEAKER_1, \
    FIELD_ALIAS_SPEAKER_2, \
    FIELD_ALIAS_TEAM


class TeamRegistrationForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = [
            'name',
        ]
        labels = {
            'name': 'Название команды',
        }

    speaker_1 = forms.EmailField(label='E-mail первого спикера', widget=forms.TextInput(attrs={'class': 'form-elem__input'}))
    speaker_2 = forms.EmailField(label='E-mail второго спикера', widget=forms.TextInput(attrs={'class': 'form-elem__input'}))

    tournament = None

    def __init__(self, tournament: Tournament, *args, **kwargs):
        self.tournament = tournament
        super(TeamRegistrationForm, self).__init__(*args, **kwargs)

    def clean_speaker_1(self):
        speaker_1 = self.cleaned_data['speaker_1']

        if not User.objects.filter(email__iexact=speaker_1).count():
            raise forms.ValidationError(u'Пользователь с таким email не зарегистрировался на сайте')

        return speaker_1

    def clean_speaker_2(self):
        speaker_2 = self.cleaned_data['speaker_2']

        if not User.objects.filter(email__iexact=speaker_2).count():
            raise forms.ValidationError(u'Пользователь с таким email не зарегистрировался на сайте')

        return speaker_2

    def clean(self):
        super(TeamRegistrationForm, self).clean()

        if not self.is_valid():
            return

        if self.cleaned_data['speaker_1'] == self.cleaned_data['speaker_2']:
            raise forms.ValidationError(u'Email первого и второго спикера должны различаться')

        team_exists = self.tournament.team_members.filter(
            speaker_1__email__iexact=self.cleaned_data['speaker_1'],
            speaker_2__email__iexact=self.cleaned_data['speaker_2']
        ).exists()

        team_exists |= self.tournament.team_members.filter(
            speaker_1__email__iexact=self.cleaned_data['speaker_2'],
            speaker_2__email__iexact=self.cleaned_data['speaker_1']
        ).exists()

        if team_exists:
            raise forms.ValidationError(u'Команда с этими спикерами уже зарегистрированна в турнире')

        if self.tournament.team_members.filter(name=self.cleaned_data['name']).exists():
            raise forms.ValidationError(u'Команда таким названием уже зарегистрированна в турнире')

    def save(self, commit=True):
        team = super(TeamRegistrationForm, self).save(commit=False)
        team.speaker_1 = User.objects.get(email__iexact=self.cleaned_data['speaker_1'])
        team.speaker_2 = User.objects.get(email__iexact=self.cleaned_data['speaker_2'])
        if commit:
            team.save()
        return team


class TeamWithSpeakerRegistrationForm(TeamRegistrationForm):

    def __init__(self, tournament: Tournament, questions=None, *args, **kwargs):
        # :questions: - Для единого интерфейса с CustomTeamRegistrationForm
        super(TeamWithSpeakerRegistrationForm, self).__init__(tournament, *args, **kwargs)
        self.fields['speaker_1'].widget.attrs['readonly'] = True
        self.fields['speaker_1'].label = 'Ваш e-mail'
        self.fields['speaker_2'].label = 'E-mail вашего напарника'

    def save(self, speaker_1=None, commit=True):
        team = super(TeamWithSpeakerRegistrationForm, self).save(commit=False)
        team.speaker_1 = speaker_1
        if commit:
            team.save()
        return team


class CustomForm:
    """
    :self.fields:
    :self._required_fields:
    :self.cleaned_data
    """

    def init_custom_fields(self, questions):
        ordered_questions = OrderedDict()
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
                    widget=forms.Textarea(attrs={'class': 'form-elem__input', 'rows': '5'}),
                    help_text=question.comment,
                    required=question.required,
                )
            ordered_questions[field_name] = self.fields[field_name]

        self.fields = ordered_questions

    def get_answers(self, questions):
        answers = {}
        for question in questions:
            if question.alias and question.alias.name in self._required_fields:
                field_name = self._required_fields[question.alias.name]
            else:
                field_name = 'question_%s' % question.position
            answers[question.question] = self.cleaned_data[field_name]

        return answers


class CustomTeamRegistrationForm(TeamWithSpeakerRegistrationForm, CustomForm):

    _required_fields = {
        FIELD_ALIAS_TEAM.name: 'name',
        FIELD_ALIAS_SPEAKER_1.name: 'speaker_1',
        FIELD_ALIAS_SPEAKER_2.name: 'speaker_2',
    }

    def __init__(self, tournament: Tournament, questions, *args, **kwargs):
        super(CustomTeamRegistrationForm, self).__init__(tournament, questions, *args, **kwargs)
        self.init_custom_fields(questions)
        self.fields['name'].widget.attrs['class'] = 'form-elem__input'


class CustomAdjudicatorRegistrationForm(forms.Form, CustomForm):

    adjudicator = forms.EmailField()

    _required_fields = {
        FIELD_ALIAS_ADJUDICATOR.name: 'adjudicator',
    }

    def __init__(self, questions, *args, **kwargs):
        super(CustomAdjudicatorRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['adjudicator'].widget.attrs['readonly'] = True
        self.init_custom_fields(questions)
        self.fields['adjudicator'].widget.attrs['class'] = 'form-elem__input'
        # self.
