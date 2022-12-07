from django.urls import reverse_lazy
from django.views.generic import UpdateView
from pedidos.models.grupo_complemento import GrupoComplementos


class GrupoComplementoUpdate(UpdateView):
    model = GrupoComplementos
    fields = '__all__'

    def get_success_url(self):
       return reverse_lazy("list_grupo_complemento")
