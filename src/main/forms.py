from django import forms

from .models import ExecutorOffer, Project, WorkerSlot


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


class WorkerSlotForm(forms.ModelForm):
    """
    Форма создания и изменения слота работника.
    """

    class Meta:
        model = WorkerSlot
        exclude = ('profile', 'project')
