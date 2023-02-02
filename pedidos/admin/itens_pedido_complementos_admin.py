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

    list_filter = [
        
    ]