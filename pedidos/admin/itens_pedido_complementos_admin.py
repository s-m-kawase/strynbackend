from pedidos.models.itens_pedido_complementos import ItensPedidoComplementos 
from django.contrib import admin


@admin.register(ItensPedidoComplementos)
class ItensPedidoComplementosAdmin(admin.ModelAdmin):
    list_display = [
        'complemento',
        'quantidade',
        'valor_unitario',
        'total',
    ]

    search_fields = [
        'valor_unitario',
        'total',
        'quantidade'
        
    ]

    list_filter = [
        'complemento'
    ]