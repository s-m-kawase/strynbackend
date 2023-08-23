from rest_framework import viewsets, filters
import django_filters.rest_framework
from pedidos.models import Cliente
from ..serializers.cliente_serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from django.http.response import JsonResponse
from rest_framework.response import Response
from ...forms import ClienteForm, UserForm
from django.contrib.auth.hashers import make_password
from rest_framework import status

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
    
    def create(self, request, *args, **kwargs):

        user_form = UserForm({
            "username": request.data.get('username',None),
            "password": make_password(request.data.get('password',None)),
        })
        
        cliente_form = ClienteForm({
            "nome_cliente": request.data.get('nome_cliente',None),
            "cpf": request.data.get('cpf',None),
            "celular": request.data.get('celular',None),
            "hash_cliente": request.data.get('hash',None),
        },request.FILES)

        success = True
        message = ''
        status_code = 1
        error_messages = []
        if user_form.is_valid():
            if cliente_form.is_valid():
                user = user_form.save()
                user.email = user_form.instance.username
                user.save()
                cliente = cliente_form.save(commit=False) 
                cliente.usuario = user  
                cliente.email = user.username  
                cliente.save()  
                message = "Cliente criado com sucesso!"
                status_code = status.HTTP_200_OK
            else:
<<<<<<< HEAD
                #outra abordagem para retornar os erros
                message = cliente_form.errors
=======
                error_messages.extend([error[0] for error in user_form.errors.values()])
                error_messages.extend([error[0] for error in cliente_form.errors.values()])
>>>>>>> c0a26b1d33a79323ffcf35bf703d26e2a4dedc40
                success = False
                status_code = status.HTTP_400_BAD_REQUEST
        else:
            
            if not cliente_form.is_valid():
                error_messages.extend([error[0] for error in cliente_form.errors.values()])
            status_code = status.HTTP_400_BAD_REQUEST
            success = False
        
        return Response({"message": error_messages if not success else message, "success": success}, status=status_code)

        

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