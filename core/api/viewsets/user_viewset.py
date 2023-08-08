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
from pedidos.api.serializers.cliente_serializers import ClienteSerializer
from pedidos.forms import ClienteForm, UserForm
from django.contrib.auth.hashers import make_password

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


class UserViewSet(ModelViewSet):
    pagination_class = StandardResultsSetPagination
    authentication_classes = (SessionAuthentication, JWTAuthentication)
    permission_classes = ()
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filterset_fields = ('id',)

    
    def update(self, request, *args, **kwargs):    
        user_instance = User.objects.get(pk=kwargs.get('pk'))
        user_form = UserForm({
            "username": request.POST.get('username',user_instance.username),
            "password": request.POST.get('password',user_instance.password),
        },instance=user_instance)
        
        cliente_instance = Cliente.objects.get(usuario=user_instance.id)

        cliente_form = ClienteForm({
            "nome_cliente": request.POST.get('nome_cliente',cliente_instance.nome_cliente),
            "cpf": request.POST.get('cpf',cliente_instance.cpf),
            "celular": request.POST.get('celular',cliente_instance.celular),
            
        },request.FILES, instance=cliente_instance)

        success = True
        message = ''

        if user_form.is_valid() and cliente_form.is_valid():
            
            user = user_form.save()
            cliente_instance.usuario = user
            user_instance.email = user.username
            user_instance.save()
            cliente_instance.email = user.username
            cliente_instance.save()
            message = "Cliente alterado com sucesso!"

        else:
            message= user_form.errors
            if not cliente_form.is_valid():
                for chave, valor in cliente_form.errors.items():
                    message[f'{chave}'] = valor
            success = False
        return JsonResponse({"message":message,"success":success})


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
    

    

    
