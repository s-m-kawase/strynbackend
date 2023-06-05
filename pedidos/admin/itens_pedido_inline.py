from django.contrib import admin
from nested_admin import nested, NestedStackedInline, NestedModelAdmin

from ..models import ItensPedido
from .item_complemento_inline import ItensPedidoComplementosInline


class ItensPedidoInline(NestedStackedInline):
    model = ItensPedido
    autocomplete_fields = ['item', 'pedido']
    readonly_fields = [
        'total_complementos',
        'preco_item_mais_complementos',
        'valor_unitario_item',
        ]
    extra = 0
    
    inlines = [
        ItensPedidoComplementosInline
    ]
