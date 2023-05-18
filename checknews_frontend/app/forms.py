from django import forms
from django.contrib.auth.models import User
from app.models import UserAccount

class UserRegisterForm(forms.Form):
    email = forms.CharField(label='email', max_length=100, required=True)
    senha = forms.CharField(label='senha', max_length=100, required=True)
    isAdministrator = False