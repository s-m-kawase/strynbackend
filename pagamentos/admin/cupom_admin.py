from pagamentos.models.cupom import Cupom
from django.contrib import admin


@admin.register(Cupom)
class CupomAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'nome',
        'porcentagem',
        'cod_cupom',
        #'validado_ate',

    ]

    search_fields = [
        'nome',
        'porcentagem',
        'id',
    ]

    list_filter = [
        'porcentagem'
    ]

    readonly_fields = [
        'status_cupom'
    ]