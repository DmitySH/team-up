from django.contrib import admin

from .models import BelbinTest, MBTITest, LSQTest


@admin.register(BelbinTest)
class BelbinAdmin(admin.ModelAdmin):
    pass


@admin.register(MBTITest)
class MBTITestAdmin(admin.ModelAdmin):
    pass


@admin.register(LSQTest)
class LSQTestAdmin(admin.ModelAdmin):
    pass
