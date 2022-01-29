from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DetailView

from .forms import ExecutorOfferForm
from src.base.services import *
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


class MainPageView(View):
    def get(self, request):
        return render(request, 'main/main_page.html')


class ExecutorOfferView(View):
    def get(self, request):
        check_auth(request)

        form = ExecutorOfferForm(instance=request.user.profile.offer())
        return render(request, 'main/executor_offer.html',
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

        return render(request, 'main/executor_offer.html',
                      context={'form': form})


def delete_offer(request):
    if request.POST:
        offer = request.user.profile.offer()
        if offer:
            offer.delete()
    return redirect(request.user.profile.get_absolute_url())
