from pedidos.models.complemento import Complementos 
from django.contrib import admin
from ..models import Restaurante, Cardapio, GrupoComplementos


@admin.register(Complementos)
class ComplementosAdmin(admin.ModelAdmin):
    list_display = [
        'nome',
        'codigo_complemento',
        'preco',
    ]

    search_fields = [
        'nome',
        'preco',
        
    ]

    list_filter = [
        'status_venda'
    ]



    def get_queryset(self, request):
        queryset = super(ComplementosAdmin, self).get_queryset(request)

        user = request.user
        restaurante = Restaurante.objects.get(usuario=user)
        cardapios = Cardapio.objects.filter(restaurante=restaurante)
        ids_grupos = []
        ids_complementos = []
        for cardapio in cardapios:
            grupos = cardapio.grupo_complementos.all()
            ids_grupos.extend([grupo.id for grupo in grupos])
        
        grupos = GrupoComplementos.objects.filter(id__in=ids_grupos)

        for grupo in grupos:
            Complementos = grupo.complemento.all()
            ids_complementos.extend([Complemento.id for Complemento in Complementos])

        queryset = queryset.filter(id__in=ids_complementos)


        return queryset