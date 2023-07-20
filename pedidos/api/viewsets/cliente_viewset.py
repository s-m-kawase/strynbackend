from rest_framework import viewsets, filters
import django_filters.rest_framework
from pedidos.models import Cliente
from ..serializers.cliente_serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from django.http.response import JsonResponse
from rest_framework.response import Response

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

class ClienteViewSet(viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    permission_classes = ()
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

    filter_backends = [filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]

    filterset_fields = []

    search_fields = ['nome_cliente']

    def check_duplicates(self, data):
        cpf = data.get('cpf', None)
        username = data.get('usuario.username', {})  
        email = data.get('email',None)

        duplicates = {}

        if Cliente.objects.filter(cpf=cpf).exists():
            duplicates.setdefault('cpf', []).append("Cliente com este CPF já existe.")

        if User.objects.filter(username=username).exists():
            duplicates.setdefault('usuario', {}).setdefault('username', []).append("Um usuário com este nome de usuário já existe.")

        if Cliente.objects.filter(email=email).exists():
            duplicates.setdefault('usuario', {}).setdefault('email', []).append("Cliente com este email já está em uso.")

        return duplicates
    
    def create(self, request, *args, **kwargs):
        duplicates = self.check_duplicates(request.data)

        if duplicates:
            return Response(duplicates, status=400)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        usuario_data = serializer.validated_data.pop('usuario')
        password = usuario_data.pop('password')
        usuario = User(**usuario_data)
        usuario.set_password(password)
        usuario.save()

      
        cliente = Cliente.objects.create(usuario=usuario, **serializer.validated_data)
        serializer.instance = cliente
        headers = self.get_success_headers(serializer.data)
        
        return Response(serializer.data, status=201, headers=headers)

        

    @action(methods=['get'], detail=False)
    def usuario_logado(self, request):

      user = request.user
      cliente = Cliente.objects.filter(usuario=user).first()
      if cliente:
        context = ({
            "id_cliente":cliente.id,
            "username":cliente.usuario.username,
            "nome":cliente.nome_cliente,
            "email":cliente.email,
            "celular":cliente.celular,
            "is_staff":cliente.usuario.is_staff,
            "is_superuser":cliente.usuario.is_superuser
        })
      else:
         context = {
            "message": "Cliente não encontrado."
        }


      return JsonResponse(context, content_type="application/json", safe=False)