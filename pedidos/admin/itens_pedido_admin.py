from pedidos.models.itens_pedido import ItensPedido 
from django.contrib import admin


@admin.register(ItensPedido)
class ItensPedidoAdmin(admin.ModelAdmin):
    list_display = [
        'quantidade',
        'valor_unitario',
        'total',
    ]

    search_fields = [
        'valor_unitario',
        'total',
        
    ]

    list_filter = [
        'valor_unitario'
    ]