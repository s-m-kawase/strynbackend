from pedidos.models.clientes import Cliente
from django.contrib import admin


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = [
        'nome_cliente',
        'historico_pedido',
    ]

    search_fields = [
        'nome_cliente'
    ]

    list_filter = [
        'historico_pedido'
    ]