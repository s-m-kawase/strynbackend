from pedidos.models.categoria_cardapio import CategoriaCardapio
from django.contrib import admin
from .ordem_categoria_cardapio_inline import OrdemCategoriaCardapioInline


@admin.register(CategoriaCardapio)
class CategoriaCardapioAdmin(admin.ModelAdmin):
    list_display = [
        'nome',
    ]

    search_fields = [
        'nome'
        
    ]

    list_filter = [
        'status'
    ]

    inlines = [OrdemCategoriaCardapioInline]