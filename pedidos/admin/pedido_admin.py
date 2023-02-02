from pedidos.models.pedido import  Pedidos
from django.contrib import admin
from .itens_pedido_inline import ItensPedidoInline

@admin.register(Pedidos)
class PedidosAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'status_pedido',
        'subtotal',
        'total'
    ]

    search_fields = [
        'id',
    ]

    filter_horizontal = [
        'tempo_estimado'
    ]

    readonly_fields = [
        'data_criacao',
    ]

    autocomplete_fields = [
        'cliente'
    ]

    inlines = [
        ItensPedidoInline
    ]