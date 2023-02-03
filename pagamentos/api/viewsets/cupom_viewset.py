from rest_framework.decorators import action
from django.http.response import JsonResponse
from rest_framework import generics, serializers, viewsets
from pagamentos.models import Cupom
from ..serializers.cupom_serializers import *
from rest_framework.permissions import IsAuthenticated
from datetime import date, datetime


class CupomViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Cupom.objects.all()
    serializer_class = CupomSerializer


    # @action(methods=['get'], detail=False)
    # def cupom_valido_ate(self, request):

    #     validos = Cupom.objects.get()
    #     cupom = []
    #     for valido in validos:

    #         try:
    #             tempo = valido.validado_ate
    #             mensagem = 'Cumpom ainda é valido'

    #         except:
    #             tempo = 0
    #             mensagem = 'Tempo de cupom excedido'
    #             return JsonResponse(
    #                 {
    #                     "cupom": mensagem
    #                 }, 
    #                 content_type="application/json",
    #                 status=400
    #             )
    #         data_atual = datetime.today()
    #         if data_atual <= tempo :
    #             return mensagem

    #         cupom.append({
    #                 "data": valido.validado_ate,
    #                 "cupom":mensagem
    #             })
    #     context = {
    #         "cupom_valido": cupom,
    #     }

    #     return JsonResponse(
    #         context, 
    #         content_type="application/json"
    #     )


