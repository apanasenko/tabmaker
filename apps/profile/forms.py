from allauth.account.forms import \
    LoginForm as DefaultLoginForm
from django import forms
from .models import \
    User, \
    Country, \
    City, \
    University


class ProfileForm(forms.ModelForm):
    country_name = forms.CharField(widget=forms.HiddenInput())
    country_id = forms.IntegerField(widget=forms.Select(), label='Страна')

    city_name = forms.CharField(widget=forms.HiddenInput())
    city_id = forms.IntegerField(widget=forms.Select(), label='Город')

    university_name = forms.CharField(widget=forms.HiddenInput())
    university_id = forms.IntegerField(widget=forms.Select(), label='Университет')

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'phone',
            'link',
            'player_experience',
            'adjudicator_experience',
        ]

        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'phone': 'Номер телефона',
            'link': 'Ваша страничка',
            'player_experience': 'Опыт в дебатах',
            'adjudicator_experience': 'Судейский опыт',
        }

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'validate'}),
            'last_name': forms.TextInput(attrs={'class': 'validate'}),
            'phone': forms.TextInput(attrs={'class': 'validate', 'type': 'tel', 'placeholder': '+79141234567'}),
            'link': forms.URLInput(attrs={'class': 'validate', 'placeholder': 'http://vk.com/id0'}),
            'player_experience': forms.Textarea(attrs={'placeholder': 'Опыт в дебатах'}),
            'adjudicator_experience': forms.Textarea(attrs={'placeholder': 'Опыт судейства дебатов'}),
        }

    @staticmethod
    def get_or_create_country(country_id, country_name):
        country = Country.objects.filter(country_id=country_id)[0]
        return country if country else Country.objects.create(country_id=country_id, name=country_name)

    @staticmethod
    def get_or_create_city(city_id, city_name):
        city = City.objects.filter(city_id=city_id)[0]
        return city if city else City.objects.create(city_id=city_id, name=city_name)

    @staticmethod
    def get_or_create_university(country, city, university_id, university_name):
        university = University.objects.filter(country=country, city=city, university_id=university_id)[0]
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
        self.fields['email'].widget = forms.EmailInput(attrs={'class': 'validate', 'placeholder': 'ilove@debate.org'})
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
        if self.instance:
            self.initial['university_name'] = self.instance.university.name
            self.initial['city_name'] = self.instance.university.city.name
            self.initial['country_name'] = self.instance.university.country.name

    def save(self, commit=True):
        user = super(EditForm, self).save(commit=False)
        user.university = self.save_university()
        if commit:
            user.save()
        return user


class LoginForm(DefaultLoginForm):

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        del self.fields['login'].widget.attrs['placeholder']
        del self.fields['password'].widget.attrs['placeholder']

        self.fields['login'].widget.attrs['class'] = u'validate'
        self.fields['password'].widget.attrs['class'] = u'validate'
