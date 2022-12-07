from pedidos.models.cardapio import Cardapio
from django.contrib import admin


@admin.register(Cardapio)
class CardapioAdmin(admin.ModelAdmin):
    list_display = [
        'nome',
        'itens',
        'categorias',
        'restaurante',
        
    ]

    search_fields = [
        'nome'
        
    ]

    list_filter = [
        'categorias'
    ]#}