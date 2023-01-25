from pedidos.models.pedido import  Pedido
from django.contrib import admin


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
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