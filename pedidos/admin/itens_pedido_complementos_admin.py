from pedidos.models.itens_pedido_complementos import ItensPedidoComplementos 
from django.contrib import admin


@admin.register(ItensPedidoComplementos)
class ItensPedidoComplementosAdmin(admin.ModelAdmin):
    list_display = [
        
        'quantidade',
        'valor_unitario',
        
    ]

    search_fields = [
        'valor_unitario',
        'quantidade'
        
    ]

    list_filter = [
        
    ]