from pedidos.models.itens_pedido import ItensPedido 
from django.contrib import admin


@admin.register(ItensPedido)
class ItensPedidoAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'item',
        'quantidade',
        
    ]

    search_fields = [
        'id',
    ]
    autocomplete_fields = ['item', 'pedido']

    readonly_fields = [
        'total_complementos',
        'preco_item_mais_complementos',
        'valor_unitario_item'
        ]