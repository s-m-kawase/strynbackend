from django.contrib import admin

from ..models import Pedidos


class PedidosInline(admin.StackedInline):
    model = Pedidos
    can_delete = False
    filter_horizontal = [ 'adicionais']
    autocomplete_fields = ['cupom']
    readonly_fields = [
        'data_criacao',
        'total',
        'subtotal'
    ]
    extra = 0
