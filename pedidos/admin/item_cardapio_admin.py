from pedidos.models.item_cardapio import ItemCardapio 
from django.contrib import admin


@admin.register(ItemCardapio)
class ItemCardapioAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'nome',
        'preco',
        'descricao',
    ]

    search_fields = [
        'id'
    ]
    
    filter_horizontal = ['categoria','grupo_complemento']