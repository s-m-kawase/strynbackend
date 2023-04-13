from django.contrib import admin
from nested_admin import nested, NestedStackedInline, NestedModelAdmin

from ..models import ItensPedido
from .item_complemento_inline import ItensPedidoComplementosInline


class ItensPedidoInline(NestedStackedInline):
    model = ItensPedido
    autocomplete_fields = ['item', 'pedido']
    readonly_fields = [
        'total_item',
        'total_complementos',
        'preco',
        ]
    extra = 0
    
    inlines = [
        ItensPedidoComplementosInline
    ]
