from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from src.accounts.models import ExecutorOffer, Profile


class AuthForm(forms.Form):
    """
    Форма входа в аккаунт.
    """

    username = forms.CharField(max_length=30, label='Имя пользователя')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')


class RegisterForm(UserCreationForm):
    """
    Форма регистрации пользователя.
    """

    username = forms.CharField(max_length=30, required=True,
                               label='Имя пользователя')
    password1 = forms.CharField(widget=forms.PasswordInput(), label='Пароль')
    password2 = forms.CharField(widget=forms.PasswordInput(),
                                label='Подтвердите пароль')

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class UserEditForm(forms.ModelForm):
    """
    Форма изменения пользователя.
    """

    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class ProfileEditForm(forms.ModelForm):
    """
    Форма изменения профиля.
    """

    class Meta:
        model = Profile
        exclude = (
            'user', 'verified', 'belbin', 'mbti', 'lsq')


class ExecutorOfferForm(forms.ModelForm):
    """
    Форма создания и изменения предложения работника.
    """

    salary = forms.IntegerField(label='Ожидаемая зарплата', required=False)

    class Meta:
        model = ExecutorOffer
        exclude = ('profile',)
