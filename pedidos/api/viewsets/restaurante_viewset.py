from rest_framework import generics, serializers, viewsets
from pedidos.models import Restaurante
from ..serializers.restaurante_serializer import RestauranteSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.http.response import JsonResponse
from datetime import date
from dateutil.relativedelta import relativedelta
class RestauranteViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Restaurante.objects.all()
    serializer_class = RestauranteSerializer

    @action(methods=['get'], detail=True)
    def relatorio_inicial(self, request, pk):
        from ...models import Pedidos
        try:

            restaurante = Restaurante.objects.get(id=pk)
            pedidos = Pedidos.objects.filter(restaurante=restaurante)

            quantidade_kda_hora = []
            pedidos_dia = []
            vendas_dia = []
            vendas_mes = []
            data_atual = date.today()
            data_inicial_semanal = data_atual - relativedelta(days=7)
            data_final_semanal = data_atual
            data_inicial_mensal = data_atual - relativedelta(months=6)
            data_final_mensal = data_atual
            
            for pedido in pedidos:
                encontrado = False
                for des in quantidade_kda_hora:
                    if des["hora"] == pedido.data_criacao.hour:
                        des["quantidade"] += 1
                        encontrado = True
                if not encontrado:
                    quantidade_kda_hora.append({
                        "hora": pedido.data_criacao.hour,
                        "quantidade": 1
                    })

            data_base_semanal = data_inicial_semanal

            while(data_base_semanal <= data_final_semanal):
                pedidos_hoje = pedidos.filter(
                        data_criacao__year=data_base_semanal.year,
                        data_criacao__month=data_base_semanal.month,
                        data_criacao__day=data_base_semanal.day
                    )
                pedidos_dia.append({
                    "data": f"{data_base_semanal.day}/{data_base_semanal.month}",
                    "quantidade": pedidos_hoje.count()
                })
                quantidade_itens = 0
                for pedido in pedidos_hoje:
                    quantidade_itens+=pedido.itens_quantidade
                
                vendas_dia.append({
                    "data": f"{data_base_semanal.day}/{data_base_semanal.month}",
                    "quantidade": quantidade_itens
                })
                

                data_base_semanal += relativedelta(days=1)

            data_base_mensal = data_inicial_mensal

            while(data_base_mensal <= data_final_mensal):
                pedidos_hoje = pedidos.filter(
                        data_criacao__year=data_base_mensal.year,
                        data_criacao__month=data_base_mensal.month
                    )

                quantidade_itens = 0
                for pedido in pedidos_hoje:
                    quantidade_itens+=pedido.itens_quantidade
                
                vendas_dia.append({
                    "data": f"{data_base_mensal.month}/{data_base_mensal.year}",
                    "quantidade": quantidade_itens
                })
                

                data_base_mensal += relativedelta(months=1)
            
            data = {
                "relatorios": {
                    "quantidade_kda_hora": quantidade_kda_hora,
                    "quantidade_pedidos_dia": pedidos_dia,
                    "quantidade_vendas_dia": vendas_dia,
                    "quantidade_vendas_mes": vendas_mes
                },
                "errors": None
            }
        except:
            data = {
                "relatorios": {},
                "errors": "Restaurante inválido."
            }
        return JsonResponse(data, content_type="application/json", safe=False)

