from django.contrib import admin
import nested_admin

from ..models import ItensPedidoComplementos


class ItensPedidoComplementosInline(nested_admin.NestedStackedInline):
    model = ItensPedidoComplementos
    # autocomplete_fields = ['item', 'pedido']
    # readonly_fields = [
    #     'total_item',
    #     'total_complementos',
    #     'preco',
    #     ]
    
    readonly_fields = [
        'valor_unitario',
    ]
    extra = 0
