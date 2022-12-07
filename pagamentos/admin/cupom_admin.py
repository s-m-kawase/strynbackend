from pagamentos.models.cupom import Cupom
from django.contrib import admin


@admin.register(Cupom)
class CupomAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'nome',
        'valor',
        'cod_cupom',
        'validado_ate',
        
    ]

    search_fields = [
        'nome',
        'valor',
        'id',
    ]

    list_filter = [
        'valor'
    ]