from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from src.accounts.models import ExecutorOffer, Profile


class AuthForm(forms.Form):
    """
    Form to log in.
    """

    username = forms.CharField(max_length=30, label='Имя пользователя')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')


class RegisterForm(UserCreationForm):
    """
    Registration form.
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
    Form which changes user's information.
    """

    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class ProfileEditForm(forms.ModelForm):
    """
    Form which changes profile's information.
    """

    class Meta:
        model = Profile
        exclude = (
            'user', 'verified', 'belbin', 'mbti', 'lsq')


class ExecutorOfferForm(forms.ModelForm):
    """
    Form of creation and changing executor offers.
    """

    salary = forms.IntegerField(label='Ожидаемая зарплата', required=False)

    class Meta:
        model = ExecutorOffer
        exclude = ('profile',)
