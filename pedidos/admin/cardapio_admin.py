from django.contrib import admin
from pedidos.models.cardapio import Cardapio, Restaurante

from .ordem_categoria_cardapio_inline import OrdemCategoriaCardapioInline


@admin.register(Cardapio)
class CardapioAdmin(admin.ModelAdmin):
    list_display = [
        "nome",
        "restaurante",
    ]

    search_fields = ["nome"]

    filter_horizontal = ["categorias"]

    autocomplete_fields = ["restaurante"]

    list_filter = []

    inlines = [OrdemCategoriaCardapioInline]

    def get_queryset(self, request):
        if request.user.is_superuser:
            queryset = super(CardapioAdmin, self).get_queryset(request)


        user = request.user
        if not user.is_superuser:

            restaurante = Restaurante.objects.get(usuario=user)

            queryset = queryset.filter(restaurante=restaurante)

            return queryset
