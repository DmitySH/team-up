from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import DetailView, ListView

from .forms import ProjectForm, WorkerSlotForm
from .models import *
from ..accounts.models import Status, ProfileProjectStatus, Profile
from ..accounts.views import SpecializationsBelbin
from ..base.services import check_own_slot, check_own_project, check_auth, \
    get_object_or_none


def delete_project(request):
    check_auth(request)
    if request.POST:
        project = request.user.profile.project()
        if project:
            project.delete()
    return redirect(request.user.profile.get_absolute_url())


def delete_slot(request, pk):
    check_auth(request)
    project = request.user.profile.project()
    if request.POST:
        slot = get_object_or_404(WorkerSlot.objects, id=pk)
        if slot.project == project:
            slot.delete()
        else:
            raise PermissionDenied
    if project:
        return redirect('project_detail', slug=project.title)
    else:
        return redirect('main_page')


class ProjectFormView(View):
    def get(self, request):
        check_auth(request)

        form = ProjectForm(instance=request.user.profile.project())
        return render(request, 'projects/project_form.html',
                      context={'form': form})

    def post(self, request):
        check_auth(request)
        project = request.user.profile.project()

        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            if project:
                form.save()
            else:
                form.instance.owner = request.user.profile
                form.save()

            return redirect('profile_detail', slug=request.user.username)

        return render(request, 'projects/project_form.html',
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
    template_name = 'projects/project_list.html'

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
    template_name = 'projects/project_detail.html'


class WorkerSlotFormView(View):
    def get(self, request, slug, pk):
        check_auth(request)
        check_own_project(request, slug)
        slot = get_object_or_none(Project.objects.get(title=slug).team,
                                  id=pk)
        form = WorkerSlotForm(instance=slot)
        return render(request, 'projects/worker_slot_form.html',
                      context={'form': form})

    def post(self, request, slug, pk):
        check_auth(request)
        check_own_project(request, slug)
        project = Project.objects.get(title=slug)
        slot = get_object_or_none(project.team, id=pk)

        form = WorkerSlotForm(request.POST, instance=slot)

        if form.is_valid():
            if slot:
                form.save()
            else:
                form.instance.project = project
                form.instance.profile = None
                form.save()

            return redirect('project_detail', slug=slug)

        return render(request, 'projects/worker_slot_form.html',
                      context={'form': form})


class ProjectInvitesView(View):
    def get(self, request, title, profile):
        check_auth(request)
        check_own_project(request, title)
        project = get_object_or_404(Project.objects, title=title)

        return render(request, 'projects/project_invite.html',
                      context={'project': project, 'username': profile})


class AppliedProfiles(View):
    def get(self, request, title, slot_pk):
        check_auth(request)
        check_own_project(request, title)
        try:
            slot = WorkerSlot.objects.get(id=slot_pk)
            check_own_slot(request, slot)

            applies = ProfileProjectStatus.objects.filter(
                worker_slot=slot,
                status=Status.objects.get(
                    value='Ожидает')).select_related('profile',
                                                     'profile__executor_offer')
            profiles = [apply.profile for apply in applies]

        except ObjectDoesNotExist:
            raise Http404
        return render(request,
                      'projects/applied_profiles_list.html',
                      context={'profiles': profiles,
                               'slot': slot})


def invite_profile(request, title, profile, slot_pk):
    check_auth(request)
    check_own_project(request, title)

    if request.POST:
        try:
            profile = Profile.objects.get(user__username=profile)
            slot = WorkerSlot.objects.get(id=slot_pk)
            check_own_slot(request, slot)
        except ObjectDoesNotExist:
            raise Http404
        same_applies = ProfileProjectStatus.objects.filter(
            profile=profile,
            worker_slot=slot,
            status=Status.objects.get(
                value='Ожидает'))
        if same_applies:
            applied = same_applies.first()
            applied.status = Status.objects.get(
                value='Приглашен')
            applied.save()
        else:
            ProfileProjectStatus.objects.get_or_create(
                profile=profile,
                worker_slot=slot,
                status=Status.objects.get(
                    value='Приглашен'))

    return redirect('offer_list')


def apply_for_slot(request, title, profile, slot_pk):
    check_auth(request)

    if request.POST:
        try:
            slot = WorkerSlot.objects.get(id=slot_pk)
        except ObjectDoesNotExist:
            raise Http404

        if ProfileProjectStatus.objects.filter(
                profile=request.user.profile,
                worker_slot=slot,
                status=Status.objects.get(
                    value='Приглашен')):
            return redirect('invitations')

        ProfileProjectStatus.objects.get_or_create(
            profile=request.user.profile,
            worker_slot=slot,
            status=Status.objects.get(
                value='Ожидает'))

    return redirect('project_detail', slug=title)


def decline_apply(request, title, profile, slot_pk):
    check_auth(request)
    check_own_project(request, title)

    if request.POST:
        try:
            profile = Profile.objects.get(user__username=profile)
            slot = WorkerSlot.objects.get(id=slot_pk)
            check_own_slot(request, slot)
        except ObjectDoesNotExist:
            raise Http404

        if slot in profile.get_applied_slots():
            apply = ProfileProjectStatus.objects.get(
                worker_slot=slot,
                profile=profile,
                status=Status.objects.get(
                    value='Ожидает'))
            apply.delete()

    return redirect(request.META.get('HTTP_REFERER'))