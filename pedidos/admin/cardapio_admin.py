from pedidos.models.cardapio import Cardapio
from django.contrib import admin


@admin.register(Cardapio)
class CardapioAdmin(admin.ModelAdmin):
    list_display = [
        'nome',
        'restaurante',
        
    ]

    search_fields = [
        'nome'
    ]
    

    filter_horizontal = [
        'categorias'
    ]

    autocomplete_fields = ['restaurante']

    list_filter = [
        
    ]