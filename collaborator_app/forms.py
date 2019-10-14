from django import forms
from . import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class LoginForm(forms.ModelForm):
    username = forms.CharField(label="", widget=forms.TextInput(attrs={"class": "form-control login-input", "placeholder": "Username"}))
    password = forms.CharField(label="", widget=forms.PasswordInput(attrs={"class": "form-control login-input", "placeholder": "Password"}))

    class Meta:
        model = models.LoginModel
        fields = ('username', 'password')

class RegisterForm(forms.ModelForm):
    first_name = forms.CharField(label="", widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "First Name"}))
    last_name = forms.CharField(label="", widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Last Name"}))
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Email"}))
    username = forms.CharField(label="", widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Username"}))
    password = forms.CharField(label="", widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password')
