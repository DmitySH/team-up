from django.db.models import Q
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DetailView, ListView

from .forms import ExecutorOfferForm, ProjectForm, WorkerSlotForm
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
        # WorkerSlot.objects.all().first().delete()
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


def delete_slot(request, pk):
    check_auth(request)
    if request.POST:
        slot = WorkerSlot.objects.filter(id=pk).first()
        if slot:
            slot.delete()
    project = request.user.profile.project()
    if project:
        return redirect('project_detail', slug=project.title)
    else:
        return redirect('main_page')


class SpecializationsBelbin:
    def get_specializations(self):
        return Specialization.objects.all()

    def get_belbin(self):
        return BelbinTest.objects.all()


class ExecutorFilterExtention(SpecializationsBelbin):
    def get_cities(self):
        return sorted([x for x in set(map(lambda x: x[0],
                                          Profile.objects.all().values_list(
                                              'city'))) if x])

    def get_remote(self):
        return sorted(
            [x for x in map(lambda x: x[1], Profile.RemoteChoices.choices)
             if x != 'Не указывать'])


class ExecutorOfferListView(ListView, ExecutorFilterExtention):
    model = ExecutorOffer
    template_name = 'main/executor_offer_list.html'

    def get_queryset(self):
        if self.request.GET:
            queryset = self.make_filter()
        else:
            queryset = ExecutorOffer.objects.all().select_related('profile')

        return queryset

    def make_filter(self):
        def convert_remote(remote):
            if remote == 'Онлайн':
                return 1
            if remote == 'И онлайн, и оффлайн':
                return 2
            if remote == 'Оффлайн':
                return 3

        cities = Q() if not self.request.GET.getlist('city') \
            else Q(profile__city__in=self.request.GET.getlist('city'))
        remote = Q() if not self.request.GET.getlist('remote') \
            else Q(profile__remote__in=[convert_remote(x) for x in
                                        self.request.GET.getlist('remote')])
        roles = Q() if not self.request.GET.getlist('role') \
            else Q(profile__belbin__role__in=self.request.GET.getlist('role'))
        specializations = Q() if not self.request.GET.getlist('specialization') \
            else Q(profile__specialization__name__in=self.request.GET.getlist(
            'specialization'))
        age = Q(
            profile__age__range=(int(self.request.GET.get('min-age') or 14),
                                 int(self.request.GET.get('max-age') or 100)
                                 )) | Q(profile__age__isnull=True)
        queryset = ExecutorOffer.objects.filter(
            cities & remote & roles & specializations & age
        ).distinct()

        return queryset


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


class ProjectFilterExtention(SpecializationsBelbin):
    def get_cities(self):
        return sorted(list(set(map(lambda x: x[0],
                                   Project.objects.all().values_list(
                                       'city')))))

    def get_remote(self):
        return sorted(list(map(lambda x: x[1], Project.REMOTE_CHOICES)))


class ProjectListView(ListView, ProjectFilterExtention):
    model = Project
    queryset = Project.objects.all()
    template_name = 'main/project_list.html'

    def get_queryset(self):
        if self.request.GET.get('search'):
            return Project.objects.filter(
                title__icontains=self.request.GET.get(
                    'search'))

        elif self.request.GET and self.request.GET.get('search') != '':
            queryset = self.make_filter()
        else:
            queryset = Project.objects.all()

        return queryset

    def make_filter(self):
        remote_chosen = [item[0] for item in Project.REMOTE_CHOICES
                         if item[1] in self.request.GET.getlist('remote')]

        if not self.request.GET.getlist('remote'):
            remote = Q()
        elif None in remote_chosen:
            remote = Q(online__isnull=True) | Q(online__in=remote_chosen)
        else:
            remote = Q(id__in=[]) | Q(online__in=remote_chosen)

        cities = Q() if not self.request.GET.getlist('city') \
            else Q(city__in=self.request.GET.getlist('city'))

        roles = Q() if not self.request.GET.getlist('role') \
            else Q(required_belbin__role__in=self.request.GET.getlist('role'))
        specializations = Q() if not self.request.GET.getlist('specialization') \
            else Q(required_specialization__name__in=self.request.GET.getlist(
            'specialization'))

        queryset = Project.objects.filter(
            cities & roles & specializations & remote).distinct()

        return queryset


class ProjectDetailView(DetailView):
    model = Project
    slug_field = 'title'
    template_name = 'main/project_detail.html'


class WorkerSlotFormView(View):
    def get(self, request, slug, pk):
        check_auth(request)
        check_own_project(request, slug)
        slot = Project.objects.get(title=slug).team.filter(id=pk).first()
        form = WorkerSlotForm(instance=slot)
        return render(request, 'main/worker_slot_form.html',
                      context={'form': form})

    def post(self, request, slug, pk):
        check_auth(request)
        check_own_project(request, slug)
        project = Project.objects.get(title=slug)
        slot = project.team.filter(id=pk).first()

        form = WorkerSlotForm(request.POST, instance=slot)

        if form.is_valid():
            if slot:
                form.save()
            else:
                slot = form.save()
                slot.project = project
                slot.profile = None
                slot.save()

            return redirect('project_detail', slug=slug)

        return render(request, 'main/worker_slot_form.html',
                      context={'form': form})
