from pagamentos.models.pagamento import Pagamento
from django.contrib import admin


@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'codigo_pagamento'
    ]

    search_fields = [
        'id',
    ]

    list_filter = [
        'codigo_pagamento'
    ]

    """ filter_horizontal = [
        'adicionais'
    ] """

    autocomplete_fields = [
        'pedido'
    ]
    
    readonly_fields = [
        'total'
    ]