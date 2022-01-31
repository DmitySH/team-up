from django import forms

from .models import ExecutorOffer, Project


class ExecutorOfferForm(forms.ModelForm):
    """
    Форма создания и изменения предложения работника.
    """

    salary = forms.IntegerField(label='Ожидаемая зарплата', required=False)

    class Meta:
        model = ExecutorOffer
        exclude = ('profile',)


class ProjectForm(forms.ModelForm):
    """
    Форма создания и изменения проекта.
    """

    class Meta:
        model = Project
        exclude = ('verified',)
