from django.contrib import admin
from core.models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False,
    verbose_name_plural = 'Profiles'
    readonly_fields = ['restaurante']
    extra = 1