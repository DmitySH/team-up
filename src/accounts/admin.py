from django.contrib import admin
from django.contrib.auth.models import User

from .models import Profile, Specialization
from src.main.models import WorkerSlot


# class WorkerSlotInline(admin.StackedInline):
#     model = WorkerSlot
#     extra = 1


# class ProfileInline(admin.StackedInline):
#     model = Profile
#     extra = 1


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass


admin.site.unregister(User)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # inlines = [ProfileInline]
    pass

@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    pass
