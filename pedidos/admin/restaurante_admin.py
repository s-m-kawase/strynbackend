from pedidos.models.restaurante import Restaurante 
from django.contrib import admin


@admin.register(Restaurante)
class RestauranteAdmin(admin.ModelAdmin):
    list_display = [
        'nome',
        'total_mesa',
        'horario_abertura',
        'horario_encerramento',
    ]

    search_fields = [
        'complemento',
        'total_mesa',
        'horario_abertura',
        'horario_encerramento',
        
    ]

    list_filter = [
        'horario_encerramento'
    ]