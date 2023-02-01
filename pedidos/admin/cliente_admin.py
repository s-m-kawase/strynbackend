from pedidos.models.clientes import Cliente
from django.contrib import admin
from .pedidos_inline import PedidosInline

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = [
        'nome_cliente',
    ]

    search_fields = [
        'nome_cliente'
    ]

    inlines = [PedidosInline]