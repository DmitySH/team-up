from django.core.exceptions import PermissionDenied
from django.shortcuts import _get_queryset
from django.urls import path, include

from config.settings import API_VERSION


def check_auth(request):
    """
    Check if user is authenticated.
    """

    if not request.user.is_authenticated:
        raise PermissionDenied


def check_own_project(request, slug):
    """
    Checks if user has project.
    """

    if request.user.profile.project:
        if request.user.profile.project.title != slug:
            raise PermissionDenied
    else:
        raise PermissionDenied


def check_own_slot(request, slot):
    """
    Check if user owns slot with slot id = slot.
    """
    if request.user.profile.project:
        if slot not in request.user.profile.project.team.all():
            raise PermissionDenied
    else:
        raise PermissionDenied


def check_slug_auth(request, slug):
    """
    Check if user has same username as in request.
    """

    check_auth(request)
    if not request.user.username == slug:
        raise PermissionDenied


def change_labels(form, labels):
    """
    Changes labels in form.
    """

    for i, field in enumerate(form.fields):
        form[field].label = labels[i]


def change_choices(form, choices):
    """
    Changes choices of form.
    """

    for i, field in enumerate(form.fields):
        form.fields[field].choices = choices[i]


def get_object_or_none(klass, *args, **kwargs):
    """
    Gets object with kwargs or None if no such object.
    """

    queryset = _get_queryset(klass)
    if not hasattr(queryset, 'get'):
        klass__name = klass.__name__ if isinstance(klass,
                                                   type) \
            else klass.__class__.__name__
        raise ValueError(
            "First argument to get_object_or_none must be a Model, Manager, "
            "or QuerySet, not '%s'." % klass__name
        )
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return None


def add_prefix_to_urls(api_urls, prefix='api/' + API_VERSION):
    """
    Adds prefix to urlpatterns list.
    """

    api_urls = [path(f'{prefix}/', include(api_urls))]
    return api_urls
