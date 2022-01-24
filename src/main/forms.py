from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

from src.main.models import Profile


class AuthForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(UserCreationForm):
    """
    Форма регистрации пользователя.
    """
    username = forms.CharField(max_length=30, required=True, label='Юзернейм')
    password1 = forms.CharField(widget=forms.PasswordInput(), label='Пароль')
    password2 = forms.CharField(widget=forms.PasswordInput(), label='Подтвердите пароль')

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user', 'verified', 'specialization', 'belbin', 'mbti', 'lsq')
