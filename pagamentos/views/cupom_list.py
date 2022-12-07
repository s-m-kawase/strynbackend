from django.views.generic import ListView
from pagamentos.models.cupom import Cupom


class CupomList(ListView):
    model = Cupom
    fileds = '__all__'

