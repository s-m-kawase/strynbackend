from pedidos.models.pedido import  Pedidos
from django.contrib import admin
from .itens_pedido_inline import ItensPedidoInline
from nested_admin import nested, NestedStackedInline, NestedModelAdmin


@admin.register(Pedidos)
class PedidosAdmin(NestedModelAdmin):
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

        'adicionais'
    ]

    readonly_fields = [
        'data_criacao',
        'subtotal',
        'total'
    ]

    autocomplete_fields = [
        'cliente',
        'cupom',

    ]

    inlines = [
        ItensPedidoInline
    ]