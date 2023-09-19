from rest_framework.decorators import action
from django.http.response import JsonResponse
from rest_framework import viewsets, filters
import django_filters.rest_framework
from pagamentos.models import Cupom
from ..serializers.cupom_serializers import *
from rest_framework.permissions import IsAuthenticated
from datetime import date, datetime
from rest_framework.pagination import PageNumberPagination
from pedidos.models import Pedidos
from django.core.exceptions import ObjectDoesNotExist

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


class CupomViewSet(viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    #permission_classes = (IsAuthenticated,)
    queryset = Cupom.objects.all()
    serializer_class = CupomSerializer

    filter_backends = [filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]

    filterset_fields = ['validado_ate']

    search_fields = ['nome']

    @action(methods=['post'], detail=False)
    def validar_cupom(self, request):
      cod_cupom = request.data.get('cod_cupom', None)
      pedido_id = request.data.get('pedido_id', None)

      try:
        cupom = Cupom.objects.get(cod_cupom=cod_cupom)
        pedido = Pedidos.objects.get(id=pedido_id)

      except ObjectDoesNotExist:
          cupom = None
          pedido = None
          cupom_valido = False
          mensagem = 'Cupom não existe'




      if cupom:
          if cupom.valido_para_aplicar():
              if cupom.aplicar_cupom(pedido):
                  cupom_valido = True
                  mensagem = 'Cupom aplicado com sucesso'
          else:
              cupom.marcar_expirado()
              mensagem = 'Cupom expirado'
              cupom_valido = False

      cupom_serializado = CupomSerializer(cupom).data if cupom else None

      return JsonResponse(
            {
                "cupom": cupom_serializado,
                "mensagem": mensagem,
                "cupom_valido": cupom_valido
            }
        )

    @action(methods=['post'], detail=False)
    def remover_cupom(self, request):
        pedido_id = request.data.get('pedido_id',None)
        try:
            pedido= Pedidos.objects.get(id=pedido_id)
            if pedido.cupom:
                pedido.cupom = None
                pedido.save()
                return JsonResponse({"mensagem": "Cupom removido com sucesso"})
            else:
                return JsonResponse({"mensagem": "Não ha cupom aplicado"})
        except Pedidos.DoesNotExist:
            raise JsonResponse({"mensagem": "Pedido não encontrados"})
        
    def get_queryset(self):
        from pedidos.models import Restaurante
        query = super().get_queryset()
        # restaurante = self.request.params.get('restaurante', None)
        user = self.request.user
        restaurante = Restaurante.objects.get(usuario=user)
        if restaurante:
            query = query.filter(restaurante=restaurante)

        return query