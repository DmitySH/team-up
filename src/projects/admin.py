from django.contrib import admin

from .models import *

"""
Register all models to admin panel.
"""


@admin.register(WorkerSlot)
class WorkerSlotAdmin(admin.ModelAdmin):
    pass


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass
