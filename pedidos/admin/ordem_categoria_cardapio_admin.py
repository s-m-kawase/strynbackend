from django.contrib import admin

from ..models import Cardapio, OrdemCategoriaCardapio, Restaurante


@admin.register(OrdemCategoriaCardapio)
class OrdemCategoriaCardapioAdmin(admin.ModelAdmin):
    list_display = ["id", "ordem", "cardapio", "categoria"]

    search_fields = ["id", "ordem", "cardapio", "categoria"]

    def get_queryset(self, request):
        if not request.user.is_superuser:
            queryset = super(OrdemCategoriaCardapioAdmin, self).get_queryset(
                request
            )

            user = request.user
            restaurante = Restaurante.objects.get(usuario=user)
            cardapios = Cardapio.objects.filter(restaurante=restaurante)
            ids_ordens = []
            for cardapio in cardapios:
                categorias = cardapio.categorias.all()

            ordens = OrdemCategoriaCardapio.objects.filter(
                categoria__in=categorias
            )
            ids_ordens.extend([ordem.id for ordem in ordens])

            queryset = queryset.filter(id__in=ids_ordens)
            return queryset
