from pedidos.models.item_cardapio import ItemCardapio 
from django.contrib import admin


@admin.register(ItemCardapio)
class ItemCardapioAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'preco',
        'foto',
        'descricao',
    ]

    search_fields = [
        'id'
    ]