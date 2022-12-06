from django.views.generic import ListView
from pedidos.models.grupo_complemento import GrupoComplementos


class GrupoComplementoList(ListView):
    model = GrupoComplementos
    fileds = '__all__'

