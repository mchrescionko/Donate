from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator

from .models import *

def LoginValidator(value):
    x = User.objects.filter(username=value)
    if len(x) != 0:
        raise ValidationError("Taki login juz istnieje")


class AddUserForm(forms.Form):
    login = forms.CharField(label="login", validators=[LoginValidator])
    password = forms.CharField(label="password", widget=forms.PasswordInput(), )
    repeat_password = forms.CharField(label="repeat_password", widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        repeat_password = cleaned_data.get('repeat_password')
        if password != repeat_password:
            raise forms.ValidationError('Hasla nie sa takie same')

    name = forms.CharField(label="name")
    surname = forms.CharField(label="surname")
    mail = forms.CharField(label="mail", validators=[EmailValidator])


class LoginForm(forms.Form):
    login = forms.CharField(label='Login', max_length=120)
    password = forms.CharField(label='Password', max_length=120, widget=forms.PasswordInput)

