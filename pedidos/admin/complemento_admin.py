from pedidos.models.complemento import Complementos 
from django.contrib import admin


@admin.register(Complementos)
class ComplementosAdmin(admin.ModelAdmin):
    list_display = [
        'nome',
        'codigo_complemento',
        'preco',
    ]

    search_fields = [
        'nome',
        'preco',
        
    ]

    list_filter = [
        'status_venda'
    ]#}