from django.views.generic import CreateView
from pedidos.models.grupo_complemento import GrupoComplementos
from django.urls import reverse_lazy


class GrupoComplementoCreate(CreateView):
    model = GrupoComplementos
    fields = '__all__'
    def get_success_url(self):
       return reverse_lazy("list_grupo_complemento")