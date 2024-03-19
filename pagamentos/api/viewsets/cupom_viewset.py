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
from django.utils import timezone


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


class CupomViewSet(viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    permission_classes = (IsAuthenticated,)
    queryset = Cupom.objects.all()
    serializer_class = CupomSerializer

    filter_backends = [filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]

    filterset_fields = ['validado_ate']

    search_fields = ['nome']

    def create(self, request, *args, **kwargs):
        cod_cupom = request.data.get('cod_cupom')

        if Cupom.objects.filter(cod_cupom=cod_cupom).exists():
            menssage = 'Falha ao criar cupom'
            error = 'Código de cupom já existe'
            success = False
            return JsonResponse({
                "menssage":menssage,
                "error":error,
                "success":success
                })
        else:
            super().create(request, *args, **kwargs)
            menssage = 'Cupom criado com sucesso' 
            error = {}
            success = True
            return JsonResponse({
                "menssage":menssage,
                "error":error,
                "success":success
                })
        
    def update(self, request, *args, **kwargs):
        cupom_id = kwargs.get('pk')
        cupom = Cupom.objects.filter(id=cupom_id).first()

        if not cupom:
            mensagem = 'Falha ao alterar cupom'
            erro = 'Cupom não encontrado'
            successo = False
            return JsonResponse({
                "mensagem": mensagem,
                "erro": erro,
                "successo": successo
            }) 

        else:
            # Pegar possíveis campos a serem alterados
            # nome = request.data.get('nome', None)
            # descricao = request.data.get('descricao', None)
            # porcentagem = request.data.get('porcentagem', None)
            cod_cupom = request.data.get('cod_cupom', None)
            validado_ate = request.data.get('validado_ate', None)
            # valor_fixo = request.data.get('valor_fixo', None)

            # Validar os dados
            if cod_cupom:
                if Cupom.objects.filter(cod_cupom=cod_cupom).exclude(pk=cupom_id).exists():
                    mensagem = 'Falha ao alterar cupom'
                    erro = 'Código de cupom já existe'
                    successo = False
                    return JsonResponse({
                        "mensagem": mensagem,
                        "erro": erro,
                        "successo": successo
                    })
            if validado_ate:
                try:
                    validado_ate = datetime.strptime(validado_ate, "%Y-%m-%dT%H:%M")
                except ValueError:
                    mensagem = 'Falha ao alterar cupom'
                    erro = 'Formato de data inválido. Use o formato: "AAAA-MM-DDTHH:MM"'
                    successo = False
                    return JsonResponse({
                        "mensagem": mensagem,
                        "erro": erro,
                        "successo": successo
                    })

            response = super().update(request, *args, **kwargs)

            return response


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
            restaurante_do_pedido = pedido.restaurante
            if cupom.restaurante == restaurante_do_pedido:
                if cupom.aplicar_cupom(pedido):
                    cupom_valido = True
                    mensagem = 'Cupom aplicado com sucesso'
            else:
                mensagem = 'Este cupom não é válido para este restaurante'
                cupom_valido = False
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