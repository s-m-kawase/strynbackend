from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from import_export.admin import ImportExportModelAdmin
from django.utils.safestring import mark_safe
from datetime import date
from core.forms import UserCreateForm

#Inlines
from core.admin import ProfileInline


admin.site.unregister(User)

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_form = UserCreateForm
    inlines = [ProfileInline]
    list_display=['id', 'username', 'email', 'is_active', 'is_staff', 'is_superuser']
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'email', 'is_staff', 'is_superuser', 'password1', 'password2', 'groups'),
        }),
    )