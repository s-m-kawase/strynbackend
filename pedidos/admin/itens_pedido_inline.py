from django.contrib import admin

from ..models import ItensPedido


class ItensPedidoInline(admin.StackedInline):
    model = ItensPedido
    autocomplete_fields = ['item', 'pedido']
    extra = 0
