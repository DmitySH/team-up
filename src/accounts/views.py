from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.views import PasswordChangeView, \
    PasswordChangeDoneView
from django.views.generic import DetailView

from src.accounts.forms import AuthForm, RegisterForm, UserEditForm, \
    ProfileEditForm
from src.accounts.models import Status, Profile
from src.base.services import check_auth, get_object_or_404
from src.main.models import ProfileProjectStatus, WorkerSlot


class LoginView(View):
    def get(self, request):
        form = AuthForm()
        return render(request, 'accounts/login.html',
                      context={'form': form})

    def post(self, request):
        form = AuthForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                return redirect('profile_detail', slug=username)
            else:
                form.add_error('__all__', 'Неверные данные!')

        return render(request, 'accounts/login.html',
                      context={'form': form})


class MyLogoutView(LogoutView):
    template_name = 'accounts/logged_out.html'


class RegisterView(View):
    def get(self, request):
        user_form = RegisterForm()
        return render(request, 'accounts/register.html',
                      context={'user_form': user_form})

    def post(self, request):
        user_form = RegisterForm(request.POST)

        if user_form.is_valid():
            user = user_form.save()
            Profile.objects.create(user=user)

            username = user_form.cleaned_data.get('username')
            raw_password = user_form.cleaned_data.get('password1')

            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect(user.profile.get_absolute_url())
        return render(request, 'accounts/register.html',
                      context={'user_form': user_form})


class UserDetailView(DetailView):
    model = User
    slug_field = 'username'
    template_name = 'accounts/user_detail.html'
    context_object_name = 'user_'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['profile'] = Profile.objects.get(user_id=context['user_'])
        return context


class MyPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/password_change.html'


class MyPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'accounts/password_change_done.html'


class UserEditView(View):
    def get(self, request):
        check_auth(request)
        form = UserEditForm(instance=request.user)
        form_profile = ProfileEditForm(instance=request.user.profile)

        args = {
            'form_user': form,
            'form_profile': form_profile,
        }
        return render(request, 'accounts/edit_profile.html', args)

    def post(self, request):
        check_auth(request)

        form = UserEditForm(request.POST, instance=request.user)
        form_profile = ProfileEditForm(request.POST, request.FILES,
                                       instance=request.user.profile)

        if form.is_valid() and form_profile.is_valid():
            if not form_profile.cleaned_data['photo']:
                request.user.profile.photo = 'profile_photos/empty.png'
                request.user.profile.save()
            form.save()
            form_profile.save()
            return redirect('profile_detail', slug=request.user.username)

        args = {
            'form_user': form,
            'form_profile': form_profile,
        }
        return render(request, 'accounts/edit_profile.html', args)


class InvitationsView(View):
    def get(self, request):
        check_auth(request)
        invited_slots = request.user.profile.get_invited_slots()
        applied_slots = request.user.profile.get_applied_slots()
        return render(request, 'accounts/invitation_list.html',
                      context={'invited_slots': invited_slots,
                               'applied_slots': applied_slots
                               })


def accept_invite(request, slot):
    check_auth(request)
    if request.POST:
        slot = get_object_or_404(WorkerSlot.objects.get(id=slot))

        if slot in request.user.profile.get_invited_slots():
            slot.profile = request.user.profile
            other_invites = ProfileProjectStatus.objects.filter(
                worker_slot=slot,
                status=Status.objects.get(
                    value='Приглашен'))
            other_invites.delete()
            slot.save()

    return redirect('invitations')


def decline_invite(request, slot):
    check_auth(request)
    if request.POST:
        slot = get_object_or_404(WorkerSlot.objects.get(id=slot))

        if slot in request.user.profile.get_invited_slots():
            invite = ProfileProjectStatus.objects.get(
                worker_slot=slot,
                profile=request.user.profile,
                status=Status.objects.get(
                    value='Приглашен'))
            invite.delete()

    return redirect('invitations')


def retract_invite(request, slot):
    check_auth(request)
    if request.POST:
        slot = get_object_or_404(WorkerSlot.objects.get(id=slot))

        if slot in request.user.profile.get_applied_slots():
            apply = ProfileProjectStatus.objects.get(
                worker_slot=slot,
                profile=request.user.profile,
                status=Status.objects.get(
                    value='Ожидает'))
            apply.delete()

    return redirect('invitations')
