from pedidos.models.iten import Item 
from django.contrib import admin


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = [
        'codigo_item',
        'preco',
        'categoria',
        'complemento',
    ]

    search_fields = [
        'preco',
        'codigo_item'
    ]

    list_filter = [
        'categoria'
    ]