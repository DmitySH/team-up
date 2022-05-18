from django import forms

from src.projects.models import Project, WorkerSlot


class ProjectForm(forms.ModelForm):
    """
    Form of creation and update of project.
    """

    class Meta:
        model = Project
        exclude = ('verified', 'owner')


class WorkerSlotForm(forms.ModelForm):
    """
    Form of creation and update of worker slot.
    """
    salary = forms.IntegerField(label='Зарплата (в рублях)', required=False)

    class Meta:
        model = WorkerSlot
        exclude = ('profile', 'project')
