from django import forms

from src.projects.models import Project, WorkerSlot


class ProjectForm(forms.ModelForm):
    """
    Форма создания и изменения проекта.
    """

    class Meta:
        model = Project
        exclude = ('verified', 'owner')


class WorkerSlotForm(forms.ModelForm):
    """
    Форма создания и изменения слота работника.
    """

    class Meta:
        model = WorkerSlot
        exclude = ('profile', 'project')
