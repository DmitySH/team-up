from rest_framework import permissions


class HasNoBelbinResult(permissions.BasePermission):
    def has_permission(self, request, view):
        return not request.user.profile.belbin.all().exists()


class HasNoMBTIResult(permissions.BasePermission):
    def has_permission(self, request, view):
        return not request.user.profile.mbti.all().exists()


class HasNoLSQResult(permissions.BasePermission):
    def has_permission(self, request, view):
        return not request.user.profile.lsq.all().exists()
