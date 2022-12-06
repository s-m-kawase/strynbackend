from django.views.generic import ListView
from pedidos.models.cardapio import Cardapio




class CadapioList(ListView):
    model = Cardapio
    fileds = '__all__'









