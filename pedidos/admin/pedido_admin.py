from pedidos.models.pedido import  Pedidos
from django.contrib import admin
from .itens_pedido_inline import ItensPedidoInline

@admin.register(Pedidos)
class PedidosAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'status_pedido',
        'cupom',
        'subtotal',
        'total'
    ]

    search_fields = [
        'id',
    ]

    list_filter = [
        'cupom',
        
    ]

    filter_horizontal = [
        'tempo_estimado'
    ]

    inlines = [
        ItensPedidoInline
    ]