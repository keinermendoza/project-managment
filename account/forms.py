from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email",)

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("email",)

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=100) 
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
