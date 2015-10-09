__author__ = 'Alexander'

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

    def save_university(self):
        country = Country.objects.get_or_create(
            country_id=self.cleaned_data['country_id'],
            name=self.cleaned_data['country_name']
        )[0]
        city = City.objects.get_or_create(
            city_id=self.cleaned_data['city_id'],
            name=self.cleaned_data['city_name'],
        )[0]
        university = University.objects.get_or_create(
            country=country,
            city=city,
            university_id=self.cleaned_data['university_id'],
            name=self.cleaned_data['university_name']
        )[0]

        return university


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
