from rest_framework import viewsets, filters
import django_filters.rest_framework
from pedidos.models import Restaurante
from ..serializers.restaurante_serializer import RestauranteSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.http.response import JsonResponse
from datetime import date
from dateutil.relativedelta import relativedelta
from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

class RestauranteViewSet(viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    permission_classes = (IsAuthenticated,)
    queryset = Restaurante.objects.all()
    serializer_class = RestauranteSerializer

    filter_backends = [filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]

    filterset_fields = ['horario_abertura','horario_encerramento']

    search_fields = ['nome']

    @action(methods=['get'], detail=True)
    def relatorio_inicial(self, request, pk):
        from ...models import Pedidos
        try:

            restaurante = Restaurante.objects.get(id=pk)
            pedidos = Pedidos.objects.filter(restaurante=restaurante)
            data_atual = date.today()
            quantidade_kda_hora = []
            pedidos_dia = []
            vendas_dia = []
            vendas_mes = []
            data_inicial_semanal = data_atual - relativedelta(days=7)
            data_final_semanal = data_atual
            data_inicial_mensal = data_atual - relativedelta(months=6)
            data_final_mensal = data_atual

            ### 1
            pedidos_hoje = pedidos.filter(
                data_criacao__year=data_atual.year,
                data_criacao__month=data_atual.month,
                data_criacao__day=data_atual.day
            )
            valor = 0
            for pedido in pedidos_hoje:
                valor += pedido.total

            total_pedidos_hoje = {
                "quantidade": pedidos_hoje.count(),
                "valor": valor
            }
            total_ticket_medio_hoje = round(float(total_pedidos_hoje.get('valor')) / (float(total_pedidos_hoje.get("quantidade")) if total_pedidos_hoje.get("quantidade") != 0 else 1), 2)

            ### 2
            pedidos_mes_atual = pedidos.filter(
                data_criacao__year=data_atual.year,
                data_criacao__month=data_atual.month
            )

            valor = 0
            for pedido in pedidos_mes_atual:
                valor += pedido.total
            
            total_pedidos_mes = {
                "quantidade": pedidos_mes_atual.count(),
                "valor": valor
            }
            total_ticket_medio_mes = round(float(total_pedidos_mes.get('valor')) / (float(total_pedidos_mes.get("quantidade")) if total_pedidos_mes.get("quantidade") != 0 else 1), 2)

            
            
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
                "nome__restaurante": restaurante.nome,
                "id__restaurante": restaurante.id,
                "imagem":restaurante.logo.url if restaurante.logo else None,
                "mes": data_atual.month,
                "total_pedidos_hoje": total_pedidos_hoje,
                "total_ticket_medio_hoje": total_ticket_medio_hoje,
                "total_pedidos_mes": total_pedidos_mes,
                "total_ticket_medio_mes": total_ticket_medio_mes,
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
    
    def get_queryset(self):
        query = super().get_queryset()

        usuario = self.request.user
        query = query.filter(usuario=usuario)

        categoria = self.request.query_params.get('categoria',None)

        if categoria:
            query = query.filter(categoria=categoria)

        return query

