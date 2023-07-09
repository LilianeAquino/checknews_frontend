from django import forms
from django.core.validators import EmailValidator

class UserRegisterForm(forms.Form):
    email = forms.CharField(label='email', max_length=100, required=True, validators=[EmailValidator()])
    senha = forms.CharField(label='senha', max_length=100, required=True)
    isAdministrator = False