from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

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
    password2 = forms.CharField(widget=forms.PasswordInput(),
                                label='Подтвердите пароль')

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
        exclude = (
            'user', 'verified', 'specialization', 'belbin', 'mbti', 'lsq')


class BelbinPartForm(forms.Form):
    answer0 = forms.IntegerField(max_value=10, min_value=0, required=True,
                                 initial=0)
    answer1 = forms.IntegerField(max_value=10, min_value=0, required=True,
                                 initial=0)
    answer2 = forms.IntegerField(max_value=10, min_value=0, required=True,
                                 initial=0)
    answer3 = forms.IntegerField(max_value=10, min_value=0, required=True,
                                 initial=5)
    answer4 = forms.IntegerField(max_value=10, min_value=0, required=True,
                                 initial=0)
    answer5 = forms.IntegerField(max_value=10, min_value=0, required=True,
                                 initial=0)
    answer6 = forms.IntegerField(max_value=10, min_value=0, required=True,
                                 initial=0)
    answer7 = forms.IntegerField(max_value=10, min_value=0, required=True,
                                 initial=5)

    error = ''

    def validate_sum(self):
        if sum(map(int, self.cleaned_data.values())) != 10:
            self.error = 'Неправильно заполнен блок'
            return False
        else:
            self.error = ''
            return True


class MBTIPartForm(forms.Form):
    answer1 = forms.TypedChoiceField(required=True, initial=1,
                                     coerce=lambda x: int(x))
    answer2 = forms.TypedChoiceField(required=True, initial=1,
                                     coerce=lambda x: int(x))
    answer3 = forms.TypedChoiceField(required=True, initial=1,
                                     coerce=lambda x: int(x))
    answer4 = forms.TypedChoiceField(required=True, initial=1,
                                     coerce=lambda x: int(x))
    answer5 = forms.TypedChoiceField(required=True, initial=1,
                                     coerce=lambda x: int(x))
    answer6 = forms.TypedChoiceField(required=True, initial=1,
                                     coerce=lambda x: int(x))
    answer7 = forms.TypedChoiceField(required=True, initial=1,
                                     coerce=lambda x: int(x))

