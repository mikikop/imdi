from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

class SignupForm(UserCreationForm):
    class Meta:      
        model = User
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2']


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(
        widget = forms.PasswordInput()
    )

class UpdateForm(forms.ModelForm):
    class Meta:      
        model = User
        fields = ['first_name', 'last_name', 'email']