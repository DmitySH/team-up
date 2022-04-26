import django.contrib.auth.password_validation as validators
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import PasswordChangeView, \
    PasswordChangeDoneView
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import DetailView, ListView
from rest_framework import generics, permissions, status, parsers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from src.base.services import get_object_or_none
from src.projects.models import WorkerSlot
from src.tests.models import BelbinTest
from . import serializers
from . import services
from .forms import AuthForm, RegisterForm, UserEditForm, \
    ProfileEditForm, ExecutorOfferForm
from .models import Status, Profile, ExecutorOffer, \
    ProfileProjectStatus, Specialization


class LoginView(View):
    """
    Authorizes user.
    """

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


class CustomLogoutView(LogoutView):
    """
    Logouts user.
    """

    template_name = 'accounts/logged_out.html'


class RegisterView(View):
    """
    View of user's registration.
    """

    def get(self, request):
        user_form = RegisterForm()
        return render(request, 'accounts/register.html',
                      context={'user_form': user_form})

    def post(self, request):
        user_form = RegisterForm(request.POST)

        if user_form.is_valid():
            user_form.save()

            username = user_form.cleaned_data.get('username')
            raw_password = user_form.cleaned_data.get('password1')

            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect(user.profile.get_absolute_url())
        return render(request, 'accounts/register.html',
                      context={'user_form': user_form})


class UserDetailView(DetailView):
    """
    View of detail information about user's profile.
    """

    model = User
    slug_field = 'username'
    template_name = 'accounts/user_detail.html'
    context_object_name = 'user_'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['profile'] = Profile.objects.get(user_id=context['user_'])
        return context


class CustomPasswordChangeView(PasswordChangeView):
    """
    Changes password.
    """

    template_name = 'accounts/password_change.html'


class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    """
    View after password change.
    """

    template_name = 'accounts/password_change_done.html'


class UserEditView(LoginRequiredMixin, View):
    """
    View of profile editing.
    """

    def get(self, request):
        form = UserEditForm(instance=request.user)
        form_profile = ProfileEditForm(instance=request.user.profile)

        args = {
            'form_user': form,
            'form_profile': form_profile,
        }
        return render(request, 'accounts/edit_profile.html', args)

    def post(self, request):
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


class InvitationsView(LoginRequiredMixin, View):
    """
    View of invited and applied slots of logged user.
    """

    def get(self, request):
        invited_slots = request.user.profile.get_invited_slots()
        applied_slots = request.user.profile.get_applied_slots()
        projects = set(request.user.profile.get_current_projects())
        return render(request, 'accounts/invitation_list.html',
                      context={'invited_slots': invited_slots,
                               'applied_slots': applied_slots,
                               'projects': projects
                               })


@login_required(login_url='/login/')
def accept_invite(request, slot):
    """
    Accepts invite with slot id = slot of user that is logged in.
    """

    if request.POST:
        slot = get_object_or_404(WorkerSlot.objects, id=slot)
        services.accept_slot_invite(slot, request.user.profile)

    return redirect('invitations')


@login_required(login_url='/login/')
def decline_invite(request, slot):
    """
    Declines invite with slot id = slot of user that is logged in.
    """

    if request.POST:
        slot = get_object_or_404(WorkerSlot.objects, id=slot)

        if slot in request.user.profile.get_invited_slots():
            invite = ProfileProjectStatus.objects.get(
                worker_slot=slot,
                profile=request.user.profile,
                status=Status.objects.get(
                    value='Приглашен'))
            invite.delete()

    return redirect('invitations')


@login_required(login_url='/login/')
def retract_invite(request, slot):
    """
    Retracts invite with slot id = slot of user that is logged in.
    """

    if request.POST:
        slot = get_object_or_404(WorkerSlot.objects, id=slot)

        if slot in request.user.profile.get_applied_slots():
            apply = ProfileProjectStatus.objects.get(
                worker_slot=slot,
                profile=request.user.profile,
                status=Status.objects.get(
                    value='Ожидает'))
            apply.delete()

    return redirect('invitations')


class SpecializationsBelbin:
    """
    Provides extra queries for specializations and belbin test objects.
    """

    def get_specializations(self):
        return Specialization.objects.all()

    def get_belbin(self):
        return BelbinTest.objects.all()


class ExecutorOfferFormView(LoginRequiredMixin, View):
    """
    View of form to create and update executor's offer.
    """

    def get(self, request):
        form = ExecutorOfferForm(instance=request.user.profile.offer)
        return render(request,
                      'accounts/executor_offer_form.html',
                      context={'form': form})

    def post(self, request):
        form = ExecutorOfferForm(request.POST,
                                 instance=request.user.profile.offer)

        if form.is_valid():
            form.cleaned_data['profile'] = request.user.profile
            ExecutorOffer.objects.update_or_create(
                profile=form.cleaned_data['profile'],
                defaults=form.cleaned_data
            )
            return redirect('profile_detail', slug=request.user.username)

        return render(request,
                      'accounts/executor_offer_form.html',
                      context={'form': form})


@login_required(login_url='/login/')
def delete_offer(request):
    """
    Deletes user's offer.
    """

    if request.POST:
        offer = request.user.profile.offer
        if offer:
            offer.delete()
    return redirect(request.user.profile.get_absolute_url())


class ExecutorFilterExtension(SpecializationsBelbin):
    """
    Filer for executor's offers.
    """

    def get_cities(self):
        return sorted([x for x in set(map(lambda x: x[0],
                                          Profile.objects.all().values_list(
                                              'city'))) if x])

    def get_remote(self):
        return sorted(
            [x for x in map(lambda x: x[1], Profile.RemoteChoices.choices)
             if x != 'Не указывать'])


class ExecutorOfferListView(ListView, ExecutorFilterExtension):
    """
    Gets all executor's offers and provides filter for them.
    """

    model = ExecutorOffer
    template_name = 'accounts/executor_offer_list.html'
    paginate_by = 10

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


# API views.
class ProfileDetailAPIView(generics.RetrieveAPIView):
    """
    Returns all information about user's profile.
    username -- profile's username.
    """

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileDetailSerializer
    lookup_field = 'user__username'
    lookup_url_kwarg = 'username'


class ProfileUpdateAPIView(generics.UpdateAPIView):
    """
    Updates profile of user that was logged in.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.ProfileUpdateSerializer

    def get_queryset(self):
        return self.request.user.profile

    def update(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        services.object_update(user, serializer.validated_data.pop('user'))

        services.object_update(user.profile, serializer.validated_data)

        return Response(serializer.data)


class ChangePasswordView(generics.UpdateAPIView):
    """
    Changes password of user that was logged in.
    """

    serializer_class = serializers.ChangePasswordSerializer
    model = User
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not user.check_password(
                serializer.validated_data.get('old_password')):
            return Response('Wrong old password', status.HTTP_400_BAD_REQUEST)

        new_pw = serializer.validated_data.get('new_password')
        try:
            validators.validate_password(password=new_pw, user=user)
        except ValidationError as ex:
            return Response(list(ex.messages),
                            status=status.HTTP_400_BAD_REQUEST)

        services.update_password(user, new_pw)
        return Response('Password changed')


class ExecutorOfferUpdateAPIView(APIView):
    """
    Updates executor's offer of user that was logged in.
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        profile = request.user.profile
        serializer = serializers.ExecutorOfferUpdateSerializer(
            data=request.data)
        serializer.is_valid(raise_exception=True)

        created = services.update_or_create_offer(profile,
                                                  serializer.validated_data)

        if created:
            return Response('Executor offer was created')
        else:
            return Response('Executor offer was updated')


class ExecutorOfferDeleteAPIView(generics.DestroyAPIView):
    """
    Deletes executor's offer of user that was logged in.
    """

    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        offer = request.user.profile.offer
        if offer:
            offer.delete()
            return Response('Offer deleted', status.HTTP_200_OK)
        else:
            return Response('No such offer', status.HTTP_400_BAD_REQUEST)


class ExecutorOfferListAPIView(generics.ListAPIView):
    """
    Gets list of all executor offers.
    """

    serializer_class = serializers.ExecutorOfferListSerializer
    queryset = ExecutorOffer.objects.all()


class AcceptInviteAPIView(APIView):
    """
    Accepts invite of logged user to slot.
    slot_id -- id of slot where invite will be accepted.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, slot_id):
        slot = get_object_or_none(WorkerSlot.objects,
                                  id=slot_id)

        if slot and services.accept_slot_invite(slot, request.user.profile):
            return Response('Invitation accepted', status=status.HTTP_200_OK)

        return Response('User was not invited',
                        status=status.HTTP_400_BAD_REQUEST)


class InvitedWorkerSlotListAPIView(generics.ListAPIView):
    """
    Gets list of all worker slots, where logged user was invited in.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = serializers.WorkerSlotListSerializer

    def get_queryset(self):
        return self.request.user.profile.get_invited_slots()


class AppliedWorkerSlotListAPIView(generics.ListAPIView):
    """
    Gets list of all worker slots, where user has applies.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = serializers.WorkerSlotListSerializer

    def get_queryset(self):
        return self.request.user.profile.get_applied_slots()


class DeclineInviteAPIView(APIView):
    """
    Declines invitation to worker slot of user that was logged in.
    slot_id -- id of slot where invite will be declined.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, slot_id):
        slot = get_object_or_none(WorkerSlot.objects, id=slot_id)
        if slot and services.decline_slot_invite(slot, request.user.profile):
            return Response('Invite declined')

        return Response('Incorrect data')


class RetractInviteAPIView(APIView):
    """
    Retracts invitation to worker slot of user that was logged in.
    slot_id -- id of slot which will be retracted.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, slot_id):
        slot = get_object_or_none(WorkerSlot.objects, id=slot_id)

        if slot and services.retract_slot_apply(slot, request.user.profile):
            return Response('Apply retracted')

        return Response('Incorrect data')


class SpecializationListAPIView(generics.ListAPIView):
    """
    Gets list of all specializations.
    """

    serializer_class = serializers.SpecializationListSerializer
    queryset = Specialization.objects.all()
