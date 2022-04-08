from django.shortcuts import render, redirect
from django.views import View
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from src.base.constants import *
from src.base.services import *
from . import services
from .forms import BelbinPartForm, MBTIPartForm, LSQPartForm
from .models import LSQTest, BelbinTest, MBTITest
from .permissions import *


class BelbinTestFormView(View):
    def get(self, request):
        check_auth(request)

        belbin_forms = [BelbinPartForm(prefix=f'form{i + 1}') for i in
                        range(len(TestQuestions.belbin))]
        for i, form in enumerate(belbin_forms):
            change_labels(form, TestQuestions.belbin[i])

        return render(request, 'tests/belbin_test.html',
                      context={'forms': belbin_forms})

    def post(self, request):
        check_auth(request)

        belbin_forms = [BelbinPartForm(request.POST, prefix=f'form{i + 1}') for
                        i in range(len(TestQuestions.belbin))]
        for i, form in enumerate(belbin_forms):
            change_labels(form, TestQuestions.belbin[i])

        correct = all(
            [form.is_valid() and form.validate_sum() for form in belbin_forms])

        if correct:
            roles = analyze_belbin(
                [form.cleaned_data for form in belbin_forms])

            for role in roles:
                request.user.profile.belbin.add(
                    BelbinTest.objects.get(role=role))
            request.user.profile.save()
            return redirect(request.user.profile.get_absolute_url())

        return render(request, 'tests/belbin_test.html',
                      context={'forms': belbin_forms})


class MBTITestFormView(View):
    def get(self, request):
        check_auth(request)

        mbti_forms = [MBTIPartForm(prefix=f'form{i + 1}') for i in
                      range(len(TestQuestions.mbti))]
        for i, form in enumerate(mbti_forms):
            change_labels(form, TestQuestions.mbti[i])
            change_choices(form, TestChoices.mbti[i])

        return render(request, 'tests/mbti_test.html',
                      context={'forms': mbti_forms})

    def post(self, request):
        check_auth(request)

        mbti_forms = [MBTIPartForm(request.POST, prefix=f'form{i + 1}') for
                      i in range(len(TestQuestions.mbti))]
        for i, form in enumerate(mbti_forms):
            change_labels(form, TestQuestions.mbti[i])
            change_choices(form, TestChoices.mbti[i])

        correct = all([form.is_valid() for form in mbti_forms])

        if correct:
            roles = analyze_mbti(
                [form.cleaned_data for form in mbti_forms])

            for role in roles:
                request.user.profile.mbti.add(
                    MBTITest.objects.get(role=role))
            request.user.profile.save()
            return redirect(request.user.profile.get_absolute_url())

        return render(request, 'tests/mbti_test.html',
                      context={'forms': mbti_forms})


class LSQTestFormView(View):
    def get(self, request):
        check_auth(request)

        lsq_forms = [LSQPartForm(prefix=f'form{i + 1}') for i in
                     range(len(TestQuestions.lsq))]
        for i, form in enumerate(lsq_forms):
            change_labels(form, TestQuestions.lsq[i])

        return render(request, 'tests/lsq_test.html',
                      context={'forms': lsq_forms})

    def post(self, request):
        check_auth(request)

        lsq_forms = [LSQPartForm(request.POST, prefix=f'form{i + 1}') for
                     i in range(len(TestQuestions.lsq))]
        for i, form in enumerate(lsq_forms):
            change_labels(form, TestQuestions.lsq[i])

        correct = all([form.is_valid() for form in lsq_forms])

        if correct:
            roles = analyze_lsq(
                [form.cleaned_data for form in lsq_forms])

            for role in roles:
                request.user.profile.lsq.add(
                    LSQTest.objects.get(role=role))

            request.user.profile.save()
            return redirect(request.user.profile.get_absolute_url())

        return render(request, 'tests/lsq_test.html',
                      context={'forms': lsq_forms})


# API views.

class BelbinProcessAPIView(APIView):
    permission_classes = [IsAuthenticated, HasNoBelbinResult]

    def post(self, request):
        correct = all(
            [services.validate_block_sum(block.values())
             for block in request.data['value']])
        if correct:
            try:
                roles = analyze_belbin(request.data['value'])
            except KeyError:
                return Response(status=status.HTTP_400_BAD_REQUEST,
                                data='Incorrect test data')

            services.update_belbin(roles, request.user.profile)
            return Response(status=status.HTTP_200_OK,
                            data=analyze_belbin(request.data['value']))
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data='Incorrect test data')


class MBTIProcessAPIView(APIView):
    permission_classes = [IsAuthenticated, HasNoMBTIResult]

    def post(self, request):
        try:
            roles = analyze_mbti(request.data['value'])
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data='Incorrect test data')

        services.update_mbti(roles, request.user.profile)

        return Response(status=status.HTTP_200_OK,
                        data=analyze_mbti(request.data['value']))


class LSQProcessAPIView(APIView):
    permission_classes = [IsAuthenticated, HasNoLSQResult]

    def post(self, request):
        try:
            roles = analyze_lsq(request.data['value'])
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data='Incorrect test data')

        services.update_lsq(roles, request.user.profile)

        return Response(status=status.HTTP_200_OK,
                        data=analyze_lsq(request.data['value']))
