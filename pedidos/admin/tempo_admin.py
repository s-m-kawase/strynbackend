from pedidos.models.tempo import TempoEstimado 
from django.contrib import admin


@admin.register(TempoEstimado)
class TempoEstimadoAdmin(admin.ModelAdmin):
    list_display = [
        'tempo',
    ]

    search_fields = [
        'tempo',
    ]

    list_filter = [
        'tempo'
    ]