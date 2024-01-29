from django.contrib import admin
from pedidos.models import CategoriaCardapio

from ..models import Cardapio, Restaurante
from .ordem_categoria_cardapio_inline import OrdemCategoriaCardapioInline


@admin.register(CategoriaCardapio)
class CategoriaCardapioAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "nome",
    ]

    search_fields = ["nome"]

    list_filter = ["status"]

    inlines = [OrdemCategoriaCardapioInline]

    def get_queryset(self, request):
        if request.user.is_superuser:
            queryset = super(CategoriaCardapioAdmin, self).get_queryset(
                request
            )

        user = request.user
        if not user.is_superuser:

            restaurante = Restaurante.objects.get(usuario=user)
            cardapios = Cardapio.objects.filter(restaurante=restaurante)
            ids_categorias = []
            for cardapio in cardapios:
                cate = cardapio.categorias.all()
                ids_categorias.extend([categoria.id for categoria in cate])


            queryset = queryset.filter(id__in=ids_categorias)

            return queryset
