from rest_framework import permissions


class HasNoBelbinResult(permissions.BasePermission):
    """
    Checks if user has already passed belbin test.
    """

    def has_permission(self, request, view):
        return not request.user.profile.belbin.all().exists()


class HasNoMBTIResult(permissions.BasePermission):
    """
    Checks if user has already passed mbti test.
    """

    def has_permission(self, request, view):
        return not request.user.profile.mbti.all().exists()


class HasNoLSQResult(permissions.BasePermission):
    """
    Checks if user has already passed lsq test.
    """

    def has_permission(self, request, view):
        return not request.user.profile.lsq.all().exists()
