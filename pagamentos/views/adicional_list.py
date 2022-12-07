from django.views.generic import ListView
from pagamentos.models.adicional import Adicional


class AdicionalList(ListView):
    model = Adicional
    fileds = '__all__'

