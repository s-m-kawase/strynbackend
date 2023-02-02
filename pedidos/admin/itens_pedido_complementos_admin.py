from pedidos.models.itens_pedido_complementos import ItensPedidoComplementos 
from django.contrib import admin


@admin.register(ItensPedidoComplementos)
class ItensPedidoComplementosAdmin(admin.ModelAdmin):
    list_display = [
        
        'quantidade',
        
        
    ]

    search_fields = [
        'quantidade'
        
    ]
    autocomplete_fields = [
        'item_pedido',
        'complemento'
    ]
    