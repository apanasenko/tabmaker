__author__ = 'Alexander'

from django.forms import ModelForm
from .models import User


class SignupForm(ModelForm):
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
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.phone = self.cleaned_data['phone']
        user.save()
