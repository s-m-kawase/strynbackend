from django.contrib import admin

from ..models import Pedidos


class PedidosInline(admin.StackedInline):
    model = Pedidos
    can_delete = False
    filter_horizontal = ['tempo_estimado']
    readonly_fields = [
        'data_criacao'
    ]
    extra = 0
