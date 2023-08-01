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

        try:
            if Cliente.objects.filter(cpf=cpf).exists():
                raise ValueError("Já existe um cliente com este CPF.")
        except ValueError as cpf_error:
            duplicates['cpf'] = {"mensagem": str(cpf_error)}

        try:
            if User.objects.filter(username=username).exists():
                raise ValueError("Já existe um cliente com este usuário.")
        except ValueError as username_error:
            duplicates['username'] = {"mensagem": str(username_error)}

        try:
            if Cliente.objects.filter(email=email).exists():
                raise ValueError("Já existe um cliente com este email.")
        except ValueError as email_error:
            duplicates['email'] = {"mensagem": str(email_error)}

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
            "id_user":cliente.usuario.id,
            "is_staff":cliente.usuario.is_staff,
            "is_superuser":cliente.usuario.is_superuser
        })
      else:
         context = {
            "message": "Cliente não encontrado."
        }


      return JsonResponse(context, content_type="application/json", safe=False)
    
    @action(methods=['post'], detail=False)
    def excluir_user(self, request):
        id_cliente = request.data.get('id_cliente',None)
        try:
            cliente = Cliente.objects.get(id=id_cliente)
            user = cliente.user
            cliente.delete()
        except Cliente.DoesNotExist:
            return JsonResponse({"message": "Cliente não encontrado"})
        except Exception as e:
            return JsonResponse({"message": f"Ocorreu um erro durante a exclusão do cliente: {str(e)}"})

        try:
            user.delete()
            return JsonResponse({"message": "Cliente e usuário excluídos com sucesso"})
        except User.DoesNotExist:
            return JsonResponse({"message": "Cliente excluído, mas o usuário não foi encontrado"})
        except Exception as e:
            return JsonResponse({"message": f"Ocorreu um erro durante a exclusão do Usuario: {str(e)}"})