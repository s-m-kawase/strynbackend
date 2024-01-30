from django.contrib import admin
from pedidos.models.grupo_complemento import GrupoComplementos

from ..models import Cardapio, Restaurante


@admin.register(GrupoComplementos)
class GrupoComplementosAdmin(admin.ModelAdmin):
    list_display = ["nome", "quantidade_minima", "quantidade_maxima"]

    search_fields = [
        "nome",
    ]

    autocomplete_fields = ["complemento"]
    list_filter = ["complemento"]

    def get_queryset(self, request):
        if not request.user.is_superuser:
            queryset = super(GrupoComplementosAdmin, self).get_queryset(
                request
            )

            user = request.user
            restaurante = Restaurante.objects.get(usuario=user)
            cardapios = Cardapio.objects.filter(restaurante=restaurante)
            ids_grupos = []
            for cardapio in cardapios:
                grupos = cardapio.grupo_complementos.all()
                ids_grupos.extend([grupo.id for grupo in grupos])

            queryset = queryset.filter(id__in=ids_grupos)

            return queryset
