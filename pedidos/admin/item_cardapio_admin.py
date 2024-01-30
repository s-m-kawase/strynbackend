from django.contrib import admin
from pedidos.models.item_cardapio import ItemCardapio

from ..models import Cardapio, Restaurante


@admin.register(ItemCardapio)
class ItemCardapioAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "nome",
        "preco",
        "descricao",
    ]

    search_fields = ["id"]

    filter_horizontal = ["categoria", "grupo_complemento"]

    def get_queryset(self, request):
        queryset = super(ItemCardapioAdmin, self).get_queryset(request)
        if not request.user.is_superuser:

            user = request.user
            restaurante = Restaurante.objects.get(usuario=user)
            cardapios = Cardapio.objects.filter(restaurante=restaurante)
            ids_itens = []
            ids_categorias = []
            for cardapio in cardapios:
                categorias = cardapio.categorias.all()
                ids_categorias.extend(
                    [categoria.id for categoria in categorias]
                )

            itens = ItemCardapio.objects.filter(categoria__in=ids_categorias)
            ids_itens.extend([item.id for item in itens])

            queryset = queryset.filter(id__in=ids_itens)

        return queryset
