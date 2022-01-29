from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.views import PasswordChangeView, \
    PasswordChangeDoneView

from src.accounts.forms import AuthForm, RegisterForm, UserEditForm, \
    ProfileEditForm
from src.base.services import check_slug_auth
from src.main.models import Profile


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

            if User.objects.get(username=username).is_active:
                if user:
                    login(request, user)
                    return redirect('profile_detail', slug=username)
                else:
                    form.add_error('__all__', 'Неверные данные!')
            else:
                form.add_error('__all__', 'Пользователь в бане!')

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
            Profile.objects.create(
                user=user,
                patronymic=user_form.cleaned_data.get('patronymic')
            )

            username = user_form.cleaned_data.get('username')
            raw_password = user_form.cleaned_data.get('password1')

            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect(user.profile.get_absolute_url())
        return render(request, 'accounts/register.html',
                      context={'user_form': user_form})


class MyPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/password_change.html'


class MyPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'accounts/password_change_done.html'


class UserEditView(View):
    def get(self, request, slug):
        check_slug_auth(request, slug)

        form = UserEditForm(instance=request.user)
        form_profile = ProfileEditForm(instance=request.user.profile)

        args = {
            'form_user': form,
            'form_profile': form_profile,
        }
        return render(request, 'accounts/edit_profile.html', args)

    def post(self, request, slug):
        check_slug_auth(request, slug)

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
