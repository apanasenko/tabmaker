__author__ = 'Alexander'

from django import forms
from .models import \
    User, \
    Country, \
    City, \
    University


class SignupForm(forms.ModelForm):

    country_name = forms.CharField(widget=forms.HiddenInput())
    country_id = forms.IntegerField(widget=forms.Select())

    city_name = forms.CharField(widget=forms.HiddenInput())
    city_id = forms.IntegerField(widget=forms.Select())

    university_name = forms.CharField(widget=forms.HiddenInput())
    university_id = forms.IntegerField(widget=forms.Select())

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone',
        ]

    def signup(self, request, user):
        # TODO Добавить проверки (телефон)
        country = Country.objects.get_or_create(
            country_id=self.cleaned_data['country_id'],
            name=self.cleaned_data['country_name']
        )[0]
        city = City.objects.get_or_create(
            city_id=self.cleaned_data['city_id'],
            name=self.cleaned_data['city_name'],
        )[0]
        user.university = University.objects.get_or_create(
            country=country,
            city=city,
            university_id=self.cleaned_data['university_id'],
            name=self.cleaned_data['university_name']
        )[0]
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.phone = self.cleaned_data['phone']
        user.save()
