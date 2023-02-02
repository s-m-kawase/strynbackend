from pedidos.models.grupo_complemento import GrupoComplementos 
from django.contrib import admin


@admin.register(GrupoComplementos)
class GrupoComplementosAdmin(admin.ModelAdmin):
    list_display = [
        'nome',
        'quantidade_minima',
        'quantidade_maxima'
    ]

    search_fields = [
        'nome',
        
    ]

    autocomplete_fields = [
        'complemento'
    ]
    list_filter = [
        'complemento'
    ]