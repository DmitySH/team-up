from django.contrib import admin

from .models import *


class ProfileInline(admin.StackedInline):
    model = Profile
    extra = 1


class WorkerSlotInline(admin.StackedInline):
    model = WorkerSlot
    extra = 1


admin.site.unregister(User)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = [ProfileInline]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    inlines = [WorkerSlotInline]


@admin.register(BelbinTest)
class BelbinAdmin(admin.ModelAdmin):
    pass


@admin.register(MBTITest)
class MBTITestAdmin(admin.ModelAdmin):
    pass


@admin.register(LSQTest)
class LSQTestAdmin(admin.ModelAdmin):
    pass


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    pass


@admin.register(ExecutorOffer)
class ExecutorOfferAdmin(admin.ModelAdmin):
    pass


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass


@admin.register(WorkerSlot)
class WorkerSlotAdmin(admin.ModelAdmin):
    pass


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    pass


@admin.register(ProfileProjectStatus)
class ProfileProjectAdmin(admin.ModelAdmin):
    pass


admin.site.site_title = 'TeamUp'
admin.site.site_header = 'TeamUp'
