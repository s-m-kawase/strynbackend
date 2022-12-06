from pagamentos.models.adicional import Adicional
from django.contrib import admin


@admin.register(Adicional)
class AdicionalAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'nome',
        'descricao',
        'valor',
        
    ]

    search_fields = [
        'nome',
        'valor',
        'id',
    ]

    list_filter = [
        'valor'
    ]