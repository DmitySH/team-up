from django.contrib import admin

from .models import *


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    pass


@admin.register(ProfileProjectStatus)
class ProfileProjectAdmin(admin.ModelAdmin):
    pass


@admin.register(ExecutorOffer)
class ExecutorOfferAdmin(admin.ModelAdmin):
    pass


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass


admin.site.unregister(User)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    pass
