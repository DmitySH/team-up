from django.db.models import Q
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


class ProjectFilterExtention:
    def get_cities(self):
        return sorted(list(set(map(lambda x: x[0],
                                   Project.objects.all().values_list(
                                       'city')))))

    def get_specializations(self):
        return Specialization.objects.all()

    def get_belbin(self):
        return BelbinTest.objects.all()

    def get_remote(self):
        return sorted(list(map(lambda x: x[1], Project.REMOTE_CHOICES)))


class ProjectListView(ListView, ProjectFilterExtention):
    model = Project
    queryset = Project.objects.all()
    template_name = 'main/project_list.html'

    def get_queryset(self):
        print(self.request.GET)
        if self.request.GET.get('search'):
            print('fsdf')
            return Project.objects.filter(
                title__icontains=self.request.GET.get(
                    'search'))

        elif self.request.GET and self.request.GET.get(
                'search') != '':
            remote_chosen = [item[0] for item in Project.REMOTE_CHOICES
                             if item[1] in self.request.GET.getlist('remote')]

            null_remote = Q(
                online__isnull=True) if None in remote_chosen else Q(id__in=[])

            queryset = Project.objects.filter(
                Q(city__in=self.request.GET.getlist('city')) |
                Q(required_specialization__name__in=self.request.GET.getlist(
                    'specialization')) |
                Q(required_belbin__role__in=self.request.GET.getlist(
                    'role')) |
                Q(online__in=remote_chosen) | null_remote

            ).distinct()
        else:
            queryset = Project.objects.all()

        return queryset


class ProjectDetailView(DetailView):
    model = Project
    slug_field = 'title'
    template_name = 'main/project_detail.html'
