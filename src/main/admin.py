from django.contrib import admin

from .models import *


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
