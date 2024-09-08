from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm, UsernameField
from django.contrib.auth.models import User

class CreateNewDevice(forms.Form):
    popis = forms.CharField(label="Popis zariadenia", max_length=200)

class CreateNewSystem(forms.Form):
    nazov = forms.CharField(label="Nazov systemu", max_length=200)
    popis = forms.CharField(label="Popis systemu", max_length=200)

class CreateDeviceForm(forms.Form):
    nazov = forms.CharField(label="Nazov zariadenia", max_length=200)
    popis = forms.CharField(label="Popis zariadenia", max_length=200, required=False)
    alias = forms.CharField(label="Prezývka zariadenia", max_length=200, required=False)

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': '', 'id': 'hello'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': '',
            'id': 'hi',
        }
))