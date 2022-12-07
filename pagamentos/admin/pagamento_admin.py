from pagamentos.models.pagamento import Pagamento
from django.contrib import admin


@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'codigo_pagamento',
        'desconto',
        'adicionais',
        'cupom',
    ]

    search_fields = [
        'id',
        'desconto',
    ]

    list_filter = [
        'codigo_pagamento',
        'desconto'
    ]