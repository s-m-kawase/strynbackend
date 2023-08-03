from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from ..serializers.user_serializer import UserSerializer
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.http.response import JsonResponse
from rest_framework.pagination import PageNumberPagination
from pedidos.models import Cliente 

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


class UserViewSet(ModelViewSet):
    pagination_class = StandardResultsSetPagination
    authentication_classes = (SessionAuthentication, JWTAuthentication)
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filterset_fields = ('id',)

    @action(methods=['get'], detail=False)
    def usuario_logado(self, request):
        dic = UserSerializer(request.user, read_only=True)
        try:
            cliente = Cliente.objects.get(usuario=request.user)
            cliente_dados = {
                "id": cliente.id,
                "nome": cliente.nome_cliente,
                "email": cliente.email,
                "celular": cliente.celular,
                "foto": cliente.foto_perfil.url if cliente.foto_perfil else None
            }
        except Cliente.DoesNotExist:
            cliente_dados = {
                "id": None,
                "nome": None,
                "email": None,
                "celular": None,
                "foto": None
            }

        context = {
            "usuario":dic.data,
            "cliente":cliente_dados
        }
        return JsonResponse(context, content_type="application/json", safe=False)
    

    

    
