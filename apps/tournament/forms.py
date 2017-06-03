from django import forms
from datetime import datetime
from . models import \
    Tournament, \
    Round

# from django import forms
from apps.tournament.models import \
    User, \
    Country, \
    City, \
    University

DATE_ATTRS = {
    'class': 'datepicker form-elem__input',
    'type': 'date',
    'placeholder': 'Дата'
}

TIME_ATTRS = {
    'class': 'timepicker form-elem__input',
    'type': 'time',
    'placeholder': 'Время'
}


class TournamentForm(forms.ModelForm):

    open_reg_date = forms.DateField(widget=forms.DateInput(attrs=DATE_ATTRS), label=u'Дата открытия регистрации')
    open_reg_time = forms.TimeField(widget=forms.DateInput(attrs=TIME_ATTRS), label=u'Время открытия регистрации')

    close_reg_date = forms.DateField(widget=forms.DateInput(attrs=DATE_ATTRS), label=u'Дата закрытия регистрации')
    close_reg_time = forms.TimeField(widget=forms.DateInput(attrs=TIME_ATTRS), label=u'Время закрытия регистрации')

    start_tour_date = forms.DateField(widget=forms.DateInput(attrs=DATE_ATTRS), label=u'Дата начала турнира')
    start_tour_time = forms.TimeField(widget=forms.DateInput(attrs=TIME_ATTRS), label=u'Время начала турнира')

    class Meta:
        model = Tournament
        fields = [
            'name',
            'location',
            'location_lon',
            'location_lat',
            'info',
            'count_rounds',
            'count_teams',
            'count_teams_in_break',
            'link',
            'is_registration_hidden',
        ]

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'validate form-elem__input'
            }),
            'location': forms.TextInput(attrs={
                'class': 'validate form-elem__input',
                'placeholder': 'Укажите место на карте',
                'readonly': 'True',
            }),
            'location_lon': forms.HiddenInput(),
            'location_lat': forms.HiddenInput(),
            'count_rounds': forms.NumberInput(attrs={
                'min': '0',
                'placeholder': 'Количество отборочных',
                'class': 'form-elem__input form-elem--low'
            }),
            'count_teams': forms.NumberInput(attrs={
                'min': '0',
                'step': 4,
                'placeholder': 'Максимум команд',
                'class': 'form-elem__input form-elem--low'
            }),
            'count_teams_in_break': forms.NumberInput(attrs={
                'min': '0',
                'step': 4,
                'placeholder': 'Выходят в плей-офф',
                'class': 'form-elem__input form-elem--low'
            }),
            'link': forms.URLInput(attrs={
                'class': 'validate form-elem__input',
                'placeholder': 'Cсылка в социальных сетях'
            }),
            'info': forms.Textarea(attrs={
                'class': 'validate form-elem__area',
                'placeholder': 'О турнире'
            }),
            'is_registration_hidden': forms.CheckboxInput(),
        }

        labels = {
            'name': 'Название турнира',
            'location': 'Место проведения',
            'count_rounds': 'Количество раундов',
            'count_teams': 'Количество команд',
            'count_teams_in_break': 'Команд break\'е',
            'link': 'Ссылка на соц.сеть',
            'info': 'О турнире',
            'is_registration_hidden': 'Скрывать информацию о зарегистрировавшихся командах до конца регистрации',
        }

    # def clean_close_reg_date(self):
    #     open_reg_date = self.cleaned_data['open_reg_date']
    #     close_reg_date = self.cleaned_data['close_reg_date']
    #
    #     if open_reg_date > close_reg_date:
    #         raise forms.ValidationError(u'Регистрация заканчивается раньше, чем открывается')
    #
    #     return close_reg_date
    #
    # def clean_start_tour_date(self):
    #     close_reg_date = self.cleaned_data['close_reg_date']
    #     start_tour_date = self.cleaned_data['start_tour_date']
    #
    #     if start_tour_date < close_reg_date:
    #         raise forms.ValidationError(u'Турнир начинается раньше, чем закрывается регистрация')
    #
    #     return close_reg_date

    def __init__(self, *args, **kwargs):
        super(TournamentForm, self).__init__(*args, **kwargs)
        if self.instance.open_reg:
            self.initial['open_reg_date'] = self.instance.open_reg.date().isoformat()
            self.initial['open_reg_time'] = self.instance.open_reg.time().isoformat()
        if self.instance.close_reg:
            self.initial['close_reg_date'] = self.instance.close_reg.date().isoformat()
            self.initial['close_reg_time'] = self.instance.close_reg.time().isoformat()
        if self.instance.start_tour:
            self.initial['start_tour_date'] = self.instance.start_tour.date().isoformat()
            self.initial['start_tour_time'] = self.instance.start_tour.time().isoformat()

    def save(self, commit=True):
        tournament = super(TournamentForm, self).save(False)
        tournament.open_reg = datetime.combine(
            self.cleaned_data['open_reg_date'],
            self.cleaned_data['open_reg_time']
        )
        tournament.close_reg = datetime.combine(
            self.cleaned_data['close_reg_date'],
            self.cleaned_data['close_reg_time']
        )
        tournament.start_tour = datetime.combine(
            self.cleaned_data['start_tour_date'],
            self.cleaned_data['start_tour_time']
        )
        if commit:
            tournament.save()
        return tournament


class RoundForm(forms.ModelForm):

    start_round_time = forms.TimeField(
        widget=forms.DateInput(attrs={'class': 'timepicker', 'type': 'time'}), label=u'Время начала раунда')

    class Meta:
        model = Round
        fields = [
            'is_closed'
        ]

        labels = {
            'is_closed': 'Закрытый раунд'
        }

        widgets = {
            'is_closed': forms.CheckboxInput(attrs={'type': 'checkbox'})
        }

    def save(self, commit=True):
        round_obj = super(RoundForm, self).save(False)
        round_obj.start_time = datetime.combine(datetime.now().date(), self.cleaned_data['start_round_time'])
        if commit:
            round_obj.save()
        return round_obj


class CheckboxForm(forms.Form):
    is_check = forms.BooleanField()
    id = forms.IntegerField(widget=forms.HiddenInput())


class СonfirmForm(forms.Form):
    message = forms.CharField(widget=forms.TextInput())


########################################################################################
# game.forms
########################################################################################

from .models import \
    Game, \
    PlayoffResult, \
    QualificationResult


class GameForm(forms.ModelForm):
    place_id = forms.IntegerField(widget=forms.HiddenInput(attrs={'class': 'place_id'}))
    place_name = ''

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

    def init_place(self, place):
        self.initial['place_id'] = place.id
        self.place_name = place.place

    def get_place_id(self):
        return self.cleaned_data['place_id']

    def save(self, commit=True):
        game = super(GameForm, self).save(commit)
        if len(self.changed_data) > 1 or len(self.changed_data) == 1 and self.changed_data[0] != 'place_id':
            QualificationResult.objects.filter(game=game).delete()

        return game


class QualificationGameResultForm(forms.ModelForm):

    min_speaker_points = 50

    class Meta:
        model = QualificationResult

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

    def clean(self):
        super(QualificationGameResultForm, self).clean()
        if not self.is_valid():
            return

        for i in ['pm', 'lo', 'mg', 'mo', 'dpm', 'dlo', 'gw', 'ow']:
            if self.cleaned_data[i + '_exist']:
                if self.cleaned_data[i] < self.min_speaker_points:
                    self.add_error(i, 'Спикерский балл не должен быть меньше %s' % self.min_speaker_points)

            else:
                self.cleaned_data[i] = 0

        places = sorted(list(map(lambda x: self.cleaned_data[x], ['og', 'oo', 'cg', 'co'])))
        a = [1, 2, 3, 4]
        if places != a:
            for i in a:
                if i not in places:
                    self.add_error('__all__', 'Не указана команда, занявшая %s место' % i)


class PlayoffGameResultForm(forms.ModelForm):

    COUNT_COMING_NEXT = 2

    class Meta:
        model = PlayoffResult

        fields = '__all__'

        labels = {}
        widgets = {
            'game': forms.HiddenInput(attrs={'class': 'game_id'}),
        }

        for i in ['og', 'oo', 'cg', 'co']:
            widgets[i] = forms.CheckboxInput(attrs={'type': 'checkbox', 'class': 'place'})

        for i in ['og_rev', 'oo_rev', 'cg_rev', 'co_rev']:
            widgets[i] = forms.CheckboxInput(attrs={'type': 'checkbox', 'class': 'reverse_speakers'})
            labels[i] = 'Спикеры выступали в обратном порядке'

    def clean(self):
        super(PlayoffGameResultForm, self).clean()
        if not self.is_valid():
            return

        if self.COUNT_COMING_NEXT != sum(map(lambda x: self.cleaned_data[x], ['og', 'oo', 'cg', 'co'])):
            self.add_error('__all__', 'В следующий раунд должны проходить две комадны')


class FinalGameResultForm(PlayoffGameResultForm):

    COUNT_COMING_NEXT = 1

    def clean(self):
        super(FinalGameResultForm, self).clean()
        if not self.is_valid():
            return

        if self.COUNT_COMING_NEXT != sum(map(lambda x: self.cleaned_data[x], ['og', 'oo', 'cg', 'co'])):
            self.add_error('__all__', 'В финале должна победить только одна команда')


class ActivateResultForm(forms.Form):
    check_game = forms.BooleanField(widget=forms.HiddenInput(attrs={'class': 'is_check_game_input'}))

    def init(self, is_admin):
        self.initial['check_game'] = not is_admin

    def is_active(self):
        return self.cleaned_data['check_game']


#######################################################################################################
# motion
#######################################################################################################

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
            'motion': forms.Textarea(attrs={'class': 'form-elem__input', 'cols': '80', 'rows': '2'}),
            'infoslide': forms.Textarea(attrs={'class': 'form-elem__input', 'cols': '80', 'rows': '6'}),
        }


# ================= profile

class ProfileForm(forms.ModelForm):
    country_name = forms.CharField(widget=forms.HiddenInput())
    country_id = forms.IntegerField(widget=forms.HiddenInput())

    city_name = forms.CharField(widget=forms.HiddenInput())
    city_id = forms.IntegerField(widget=forms.HiddenInput())

    university_name = forms.CharField(widget=forms.HiddenInput())
    university_id = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'phone',
            'link',
            'player_experience',
            'adjudicator_experience',
            'is_show_phone',
            'is_show_email',
        ]

        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'phone': 'Номер телефона',
            'link': 'Ваша страничка',
            'player_experience': 'Опыт в дебатах',
            'adjudicator_experience': 'Судейский опыт',
            'is_show_phone': 'Телефон виден всем',
            'is_show_email': 'Email виден всем',
        }

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'validate form-elem__input'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'validate form-elem__input'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'validate form-elem__input',
                'type': 'tel',
                'placeholder': '+7914 123 45 67'
            }),
            'link': forms.URLInput(attrs={
                'class': 'validate form-elem__input',
                'placeholder': 'Например, http://vk.com/id0'
            }),
            'player_experience': forms.Textarea(attrs={
                'class': 'validate form-elem__input',
                'placeholder': 'Опыт в дебатах',
                'rows': '5'
            }),
            'adjudicator_experience': forms.Textarea(attrs={
                'class': 'validate form-elem__input',
                'placeholder': 'Опыт судейства дебатов', 'rows': '5'
            }),
            'is_show_phone': forms.CheckboxInput(),
            'is_show_email': forms.CheckboxInput(),
        }

    @staticmethod
    def get_or_create_country(country_id, country_name):
        country = Country.objects.filter(country_id=country_id).last()
        return country if country else Country.objects.create(country_id=country_id, name=country_name)

    @staticmethod
    def get_or_create_city(city_id, city_name):
        city = City.objects.filter(city_id=city_id).last()
        return city if city else City.objects.create(city_id=city_id, name=city_name)

    @staticmethod
    def get_or_create_university(country, city, university_id, university_name):
        university = University.objects.filter(country=country, city=city, university_id=university_id).last()
        return university if university else University.objects.create(
            country=country, city=city,
            university_id=university_id,
            name=university_name
        )

    def save_university(self):
        return self.get_or_create_university(
            self.get_or_create_country(self.cleaned_data['country_id'], self.cleaned_data['country_name']),
            self.get_or_create_city(self.cleaned_data['city_id'], self.cleaned_data['city_name']),
            self.cleaned_data['university_id'],
            self.cleaned_data['university_name']
        )


class SignupForm(ProfileForm):

    class Meta:
        model = User
        fields = ProfileForm.Meta.fields + ['email']

        labels = ProfileForm.Meta.labels

        widgets = ProfileForm.Meta.widgets

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget = forms.EmailInput(attrs={
            'class': 'validate form-elem__input',
            'placeholder': 'ilove@debate.org'
        })
        del self.fields['password1'].widget.attrs['placeholder']
        del self.fields['password2'].widget.attrs['placeholder']

    def signup(self, request, user):
        # TODO Добавить проверки (телефон)
        user.university = self.save_university()
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.phone = self.cleaned_data['phone']
        user.player_experience = self.cleaned_data['player_experience']
        user.adjudicator_experience = self.cleaned_data['adjudicator_experience']
        user.link = self.cleaned_data['link']
        user.save()


class EditForm(ProfileForm):

    def __init__(self, *args, **kwargs):
        super(EditForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.university is not None:
            self.initial['university_name'] = self.instance.university.name
            self.initial['university_id'] = self.instance.university.university_id
            self.initial['city_name'] = self.instance.university.city.name
            self.initial['city_id'] = self.instance.university.city.city_id
            self.initial['country_name'] = self.instance.university.country.name
            self.initial['country_id'] = self.instance.university.country.country_id

    def save(self, commit=True):
        user = super(EditForm, self).save(commit=False)
        user.university = self.save_university()
        if commit:
            user.save()
        return user


from allauth.account.forms import LoginForm as DefaultLoginForm


class LoginForm(DefaultLoginForm):

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        del self.fields['login'].widget.attrs['placeholder']
        del self.fields['password'].widget.attrs['placeholder']

        self.fields['login'].widget.attrs['class'] = u'validate'
        self.fields['password'].widget.attrs['class'] = u'validate'
