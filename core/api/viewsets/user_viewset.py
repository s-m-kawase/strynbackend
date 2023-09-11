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
        cliente_instance = Cliente.objects.get(usuario=user_instance.id)

        user_fields = {}
        cliente_fields = {}
        
        if  request.POST.get('username',False):
            user_fields['username'] = request.POST.get('username')
        else:
            user_fields['username'] = user_instance.username

        if request.POST.get('password',False):
            raw_password = request.POST.get('password')
            hashed_password = make_password(raw_password)
            user_fields['password'] = hashed_password
        else:
            user_fields['password'] = user_instance.password

        if request.POST.get('nome_cliente',False):
            cliente_fields['nome_cliente'] = request.POST.get('nome_cliente')
        else:
            cliente_fields['nome_cliente'] = cliente_instance.nome_cliente

        if request.POST.get('cpf',False):
            cliente_fields['cpf'] =request.POST.get('cpf')
        else:
            cliente_fields['cpf'] = cliente_instance.cpf

        if request.POST.get('celular',False):
            cliente_fields['celular'] =request.POST.get('celular')
        else:
            cliente_fields['celular'] = cliente_instance.celular

        if request.POST.get('email',False):
            cliente_fields['email'] = request.POST.get('email')
        else:
            cliente_fields['email'] = cliente_instance.email

        user_form = UserForm(user_fields,instance=user_instance)
        cliente_form = ClienteForm(cliente_fields,request.FILES, instance=cliente_instance)

        success = True
        message = ''
        error_messages = {}

        if user_form.is_valid() and cliente_form.is_valid():
                user_form.save()
                cliente_instance.usuario = user_form.instance
                cliente_form.save()
                user_instance.email = cliente_form.instance.email
                user_instance.save()
                message = "Cliente alterado com sucesso!"
                return JsonResponse({
                        "message": message,
                        "error":error_messages,
                        "success": success
                      })
        else:
                error_messages = {}
                for field, messages in user_form.errors.items():
                    if field not in error_messages:
                        error_messages[field] = messages[0]

                for field, messages in cliente_form.errors.items():
                    if field not in error_messages:
                        error_messages[field] = messages[0]

                message = "Falha ao alterar usuário!"
                success = False
                return JsonResponse({
                    "message": message,
                    "error": error_messages,
                    "success":success
                    })

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
                "foto": cliente.foto_perfil.url if cliente.foto_perfil else None,
                "hash_cliente": cliente.hash_cliente if cliente.hash_cliente else None,
            }
        except Cliente.DoesNotExist:
            cliente_dados = {
                "id": None,
                "nome": None,
                "email": None,
                "celular": None,
                "foto": None,
                "hash_cliente": None,
            }

        context = {
            "usuario":dic.data,
            "cliente":cliente_dados
        }
        return JsonResponse(context, content_type="application/json", safe=False)
    
    @action(methods=['put'],detail=True)
    def alterar_senha(self,request, pk):
        atual = request.data.get('senha_atual', None)
        nova = request.data.get('senha_nova', None)

        try:
            user = User.objects.get(id=pk)
            if user.check_password(atual):
                user.set_password(nova)
                user.save()
                return JsonResponse({"message": "Senha alterada com sucesso"})
            else:
                return JsonResponse({"message": "Senha atual incorreta"}, status=400)
        except User.DoesNotExist:
            return JsonResponse({"message": "Usuario não encontrado"}, status=404)

        
    

    

    
