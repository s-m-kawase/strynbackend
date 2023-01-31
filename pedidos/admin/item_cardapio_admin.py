from pedidos.models.item_cardapio import ItemCardapio 
from django.contrib import admin


@admin.register(ItemCardapio)
class ItemCardapioAdmin(admin.ModelAdmin):
    list_display = [
        'codigo_item',
        'preco',
        
        
        'foto',
        'descricao',
    ]

    search_fields = [
        'preco',
        'codigo_item'
    ]

    list_filter = [
        
    ]