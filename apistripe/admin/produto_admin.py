from django.contrib import admin

from ..models import Produto


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'produto',
        'strip_produto_id'
    ]

    search_fields = [
        'id',
        'produto'
    ]

    list_filter = [
        'produto'
    ]

   
