from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.views import PasswordChangeView, \
    PasswordChangeDoneView

from src.accounts.forms import AuthForm, RegisterForm
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
            # todo: uncomment
            # user = authenticate(username=username, password=raw_password)
            # login(request, user)
            return redirect(user.profile.get_absolute_url())
        return render(request, 'accounts/register.html',
                      context={'user_form': user_form})


class MyPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/password_change.html'


class MyPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'accounts/password_change_done.html'
