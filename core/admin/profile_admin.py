from core.models.profile import Profile
from django.contrib import admin


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'usuario',
        'email',
        'data_registro'
    ]

    search_fields = [
        'id',
        'email'
    ]

    list_filter = [
        'data_registro'
    ]

   #list_select_related = [
    #    'campos_dos_campos_fk'
    #]

   # autocomplete_fields = [
   #     'campos_fk'
   # ]
