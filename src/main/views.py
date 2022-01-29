from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DetailView

from ..base.services import *
from ..base.constants import *
from .forms import *
from .models import *


class UserDetailView(DetailView):
    model = User
    slug_field = 'username'
    template_name = 'main/user_detail.html'
    context_object_name = 'user_'

    def get(self, request, *args, **kwargs):
        check_auth(request)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['profile'] = Profile.objects.get(user_id=context['user_'])
        return context


class UserEditView(View):
    def get(self, request, slug):
        check_slug_auth(request, slug)

        form = UserEditForm(instance=request.user)
        form_profile = ProfileEditForm(instance=request.user.profile)
        args = {
            'form_user': form,
            'form_profile': form_profile,
        }
        return render(request, 'main/edit_profile.html', args)

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
        return render(request, 'main/edit_profile.html', args)


class MainPageView(View):
    def get(self, request):
        return render(request, 'main/main_page.html')


class BelbinTestFormView(View):
    def get(self, request):
        check_auth(request)

        belbin_forms = [BelbinPartForm(prefix=f'form{i + 1}') for i in
                        range(len(TestQuestions.belbin))]
        for i, form in enumerate(belbin_forms):
            change_labels(form, TestQuestions.belbin[i])

        return render(request, 'main/belbin_test.html',
                      context={'forms': belbin_forms})

    def post(self, request):
        check_auth(request)

        belbin_forms = [BelbinPartForm(request.POST, prefix=f'form{i + 1}') for
                        i in range(len(TestQuestions.belbin))]
        for i, form in enumerate(belbin_forms):
            change_labels(form, TestQuestions.belbin[i])

        correct = True

        for form in belbin_forms:
            if not form.is_valid() or not form.validate_sum():
                correct = False

        if correct:
            roles = analyze_belbin(
                [form.cleaned_data for form in belbin_forms])

            for role in roles:
                request.user.profile.belbin.add(
                    BelbinTest.objects.get(role=role))
            request.user.profile.save()
            return redirect(request.user.profile.get_absolute_url())

        return render(request, 'main/belbin_test.html',
                      context={'forms': belbin_forms})


class MBTITestFormView(View):
    def get(self, request):
        check_auth(request)

        mbti_forms = [MBTIPartForm(prefix=f'form{i + 1}') for i in
                      range(len(TestQuestions.mbti))]
        for i, form in enumerate(mbti_forms):
            change_labels(form, TestQuestions.mbti[i])
            change_choices(form, TestChoices.mbti[i])

        return render(request, 'main/mbti_test.html',
                      context={'forms': mbti_forms})

    def post(self, request):
        check_auth(request)

        mbti_forms = [MBTIPartForm(request.POST, prefix=f'form{i + 1}') for
                      i in range(len(TestQuestions.mbti))]
        for i, form in enumerate(mbti_forms):
            change_labels(form, TestQuestions.mbti[i])
            change_choices(form, TestChoices.mbti[i])

        correct = True

        for form in mbti_forms:
            if not form.is_valid():
                correct = False

        if correct:
            roles = analyze_mbti(
                [form.cleaned_data for form in mbti_forms])

            for role in roles:
                request.user.profile.mbti.add(
                    MBTITest.objects.get(role=role))
            request.user.profile.save()
            return redirect(request.user.profile.get_absolute_url())

        return render(request, 'main/mbti_test.html',
                      context={'forms': mbti_forms})


class LSQTestFormView(View):
    def get(self, request):
        check_auth(request)

        lsq_forms = [LSQPartForm(prefix=f'form{i + 1}') for i in
                     range(len(TestQuestions.lsq))]
        for i, form in enumerate(lsq_forms):
            change_labels(form, TestQuestions.lsq[i])

        return render(request, 'main/lsq_test.html',
                      context={'forms': lsq_forms})

    def post(self, request):
        check_auth(request)

        lsq_forms = [LSQPartForm(request.POST, prefix=f'form{i + 1}') for
                     i in range(len(TestQuestions.lsq))]
        for i, form in enumerate(lsq_forms):
            change_labels(form, TestQuestions.lsq[i])

        correct = True

        for form in lsq_forms:
            if not form.is_valid():
                correct = False

        if correct:
            roles = analyze_lsq(
                [form.cleaned_data for form in lsq_forms])

            for role in roles[::-1]:
                request.user.profile.lsq.add(
                    LSQTest.objects.get(role=role))

            request.user.profile.save()
            return redirect(request.user.profile.get_absolute_url())

        return render(request, 'main/lsq_test.html',
                      context={'forms': lsq_forms})
