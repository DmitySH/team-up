from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DetailView

from .forms import *
from .models import *


class MyLogoutView(LogoutView):
    next_page = '/'


class LoginView(View):
    def get(self, request):
        form = AuthForm()
        return render(request, 'main/login.html', context={'form': form})

    def post(self, request):
        form = AuthForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    login(request, user)
                    return redirect('profile_detail', slug=username)
                else:
                    form.add_error('__all__', 'Пользователь в бане!')
            else:
                form.add_error('__all__', 'Неверные данные!')
        return render(request, 'main/login.html', context={'form': form})


class UserDetailView(DetailView):
    model = User
    slug_field = 'username'
    template_name = 'main/user_detail.html'
    context_object_name = 'user_'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['profile'] = Profile.objects.get(user_id=context['user_'])
        return context


class UserFormView(View):
    def get(self, request):
        user_form = RegisterForm()
        return render(request, 'main/register.html',
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
            return HttpResponseRedirect(user.profile.get_absolute_url())
        return render(request, 'main/register.html',
                      context={'user_form': user_form})


class UserEditView(View):
    def get(self, request, slug):
        if not request.user.is_authenticated or \
                slug != request.user.username:
            raise PermissionDenied

        form = UserEditForm(instance=request.user)
        form_profile = ProfileEditForm(instance=request.user.profile)
        args = {
            'form_user': form,
            'form_profile': form_profile,
        }
        return render(request, 'main/edit_profile.html', args)

    def post(self, request, slug):
        if not request.user.is_authenticated or \
                slug != request.user.username:
            raise PermissionDenied
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
        return render(request, 'main/edit_profile.html', args)


class MainPageView(View):
    def get(self, request):
        return render(request, 'main/main_page.html')
