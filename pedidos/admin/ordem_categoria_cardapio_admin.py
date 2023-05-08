from django.contrib import admin

from ..models import OrdemCategoriaCardapio


@admin.register(OrdemCategoriaCardapio)
class OrdemCategoriaCardapioAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'ordem',
        'cardapio',
        'categoria'
    ]

    search_fields = [
        'id',
        'ordem',
        'cardapio',
        'categoria'
    ]

