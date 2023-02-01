from django.contrib import admin

from ..models import ItensPedido


class ItensPedidoInline(admin.StackedInline):
    model = ItensPedido
    extra = 0
