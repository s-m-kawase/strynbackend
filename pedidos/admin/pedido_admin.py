from pedidos.models.pedido import  Pedidos
from django.contrib import admin


@admin.register(Pedidos)
class PedidosAdmin(admin.ModelAdmin):
    list_display = [
        'numero_pedido',
        'pagamento',
        'status_pedido',
        'cupom',
        'sub_total',
        'total',
    ]

    search_fields = [
        'numero_pedido',
        
        
    ]

    list_filter = [
        'cupom',
        
    ]