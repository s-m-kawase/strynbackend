from pedidos.models.restaurante import Restaurante
from django.contrib import admin


@admin.register(Restaurante)
class RestauranteAdmin(admin.ModelAdmin):
    list_display = [
        'id',
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

    filter_horizontal = [
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
            'Dados Funcionamentos',
            {
                'fields': [
                    'horario_abertura',
                    'horario_encerramento',
                    'total_mesa',
                    'num_obrigatorio',
                    'tempo_estimado',
                    'categoria',
                    'link_restaurante',
                    'tempo_ideal',
                    'tempo_medio',
                    'tempo_limite',
                    'chave_connect',
                    'chave_asaas',
                    'pocentagem_para_tranferencia',
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

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(usuario=request.user)

    