from django.contrib import admin

from ..models import Pedidos


class PedidosInline(admin.StackedInline):
    model = Pedidos
    can_delete = False
    filter_horizontal = ['tempo_estimado']
    extra = 0
