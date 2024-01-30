from django.contrib import admin
from nested_admin import NestedModelAdmin, NestedStackedInline, nested
from pedidos.models.pedido import Pedidos

from ..models import Restaurante
from .itens_pedido_inline import ItensPedidoInline


@admin.register(Pedidos)
class PedidosAdmin(NestedModelAdmin):
    list_display = ["id", "status_pedido", "subtotal", "total"]

    search_fields = [
        "id",
    ]

    filter_horizontal = ["adicionais"]

    readonly_fields = ["data_criacao", "subtotal", "total"]

    autocomplete_fields = [
        "cliente",
        "cupom",
    ]

    inlines = [ItensPedidoInline]

    def get_queryset(self, request):
        queryset = super(PedidosAdmin, self).get_queryset(request)
        if not request.user.is_superuser:

            user = request.user
            restaurante = Restaurante.objects.get(usuario=user)

            queryset = queryset.filter(restaurante=restaurante)

        return queryset
