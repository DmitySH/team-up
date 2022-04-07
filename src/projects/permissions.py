from rest_framework import permissions


class IsSlotOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj in request.user.profile.project().team.all()


class IsProjectOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.profile.project()
