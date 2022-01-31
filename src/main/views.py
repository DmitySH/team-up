from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DetailView, ListView

from .forms import ExecutorOfferForm, ProjectForm
from src.base.services import *
from .models import *


class UserDetailView(DetailView):
    model = User
    slug_field = 'username'
    template_name = 'main/user_detail.html'
    context_object_name = 'user_'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['profile'] = Profile.objects.get(user_id=context['user_'])
        return context


class MainPageView(View):
    def get(self, request):
        return render(request, 'main/main_page.html')


class ExecutorOfferFormView(View):
    def get(self, request):
        check_auth(request)

        form = ExecutorOfferForm(instance=request.user.profile.offer())
        return render(request, 'main/executor_offer_form.html',
                      context={'form': form})

    def post(self, request):
        check_auth(request)
        form = ExecutorOfferForm(request.POST,
                                 instance=request.user.profile.offer())

        if form.is_valid():
            form.cleaned_data['profile'] = request.user.profile
            ExecutorOffer.objects.update_or_create(
                profile=form.cleaned_data['profile'],
                defaults=form.cleaned_data
            )
            return redirect('profile_detail', slug=request.user.username)

        return render(request, 'main/executor_offer_form.html',
                      context={'form': form})


def delete_offer(request):
    check_auth(request)
    if request.POST:
        offer = request.user.profile.offer()
        if offer:
            offer.delete()
    return redirect(request.user.profile.get_absolute_url())


def delete_project(request):
    check_auth(request)
    if request.POST:
        project = request.user.profile.project()
        if project:
            project.delete()
    return redirect(request.user.profile.get_absolute_url())


class ExecutorOfferListView(ListView):
    model = ExecutorOffer
    queryset = ExecutorOffer.objects.all().select_related('profile')
    template_name = 'main/executor_offer_list.html'


class ProjectFormView(View):
    def get(self, request):
        check_auth(request)

        form = ProjectForm(instance=request.user.profile.project())
        return render(request, 'main/project_form.html',
                      context={'form': form})

    def post(self, request):
        check_auth(request)
        project = request.user.profile.project()

        form = ProjectForm(request.POST, instance=project)

        if form.is_valid():
            if project:
                form.save()
            else:
                project = form.save()
                ProfileProjectStatus.objects.create(
                    profile=request.user.profile,
                    project=project,
                    status=Status.objects.get(
                        value='Создатель'))

            return redirect('profile_detail', slug=request.user.username)

        return render(request, 'main/project_form.html',
                      context={'form': form})


class ProjectListView(ListView):
    model = Project
    queryset = Project.objects.all()
    template_name = 'main/project_list.html'


class ProjectDetailView(DetailView):
    model = Project
    slug_field = 'title'
    template_name = 'main/project_detail.html'





