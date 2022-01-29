from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView

from ..base.services import *
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
