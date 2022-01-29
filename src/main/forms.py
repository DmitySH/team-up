from django import forms

from .models import ExecutorOffer


class ExecutorOfferForm(forms.ModelForm):
    """
    Форма создания и изменения предложения работника.
    """
    salary = forms.IntegerField(label='Ожидаема зарплата', required=False)

    class Meta:
        model = ExecutorOffer
        exclude = ('profile',)
