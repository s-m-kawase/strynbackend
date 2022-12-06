from pedidos.models.grupo_complemento import GrupoComplementos 
from django.contrib import admin


@admin.register(GrupoComplementos)
class GrupoComplementosAdmin(admin.ModelAdmin):
    list_display = [
        'nome',
        'complemento',
        'quantidade',
    ]

    search_fields = [
        'nome',
        
    ]

    list_filter = [
        'complemento'
    ]