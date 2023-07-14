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

    filter_horizontal=[
        'usuario',
    ]

    fieldsets = [
    (
        'Dados Restaurante',
        {
            'fields': [
                'nome',
                'descricao',
                'razao_social',
                'inscricao_estadual',
                'inscricao_municipal',
                'cnpj',
                'logo',
                'baner',

            ]
        }
    ),
    (
        'Dados Localização',
        {
            'fields': [
                'rua',
                'numero',
                'complemento',
                'bairro',
                'cep',
                'uf',
                'cidade',

            ]
        }
    ),
    (
        'Dados Funcinamentos',
        {
            'fields': [
                'horario_abertura',
                'horario_encerramento',
                'total_mesa',
                'num_obrigatorio',
                'tempo_estimado',
                'taxa_servico',
                'categoria',
                'link_restaurante',
                'usuario',
            ]
        }
    ),
    (
        'Dados Bancários',
        {
            'fields': [
                'agencia',
                'conta',
                'digito',
                'banco',
                'cvc',
            ]
        }
    ),
]