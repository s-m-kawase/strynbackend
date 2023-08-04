from rest_framework import serializers
from core.models.profile import Profile 
from pedidos.models import Cliente

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class UserByClienteSerializer(serializers.ModelSerializer):
    

    def get_groups(self, obj):
        grupos = obj.groups.values_list('name',flat = True)
        return list(grupos)
        
    def get_permissions_by_user(self, obj):
        permissoes =[] 
        for permissao in obj.user_permissions.values_list('name',flat = True):
            permissoes.append(permissao)
        for group in obj.groups.all():
            for permissao in group.permissions.all().values_list('name',flat = True):
                permissoes.append(permissao)

        return list(set(permissoes))

    class Meta:
        model = User
        fields = ['username','password',]
        read_only_fields = ('email',) 

class ClienteSerializer(serializers.ModelSerializer):
    usuario = UserByClienteSerializer()
    email = serializers.ReadOnlyField()


    # usuario_read = serializers.SerializerMethodField()

    # def get_usuario_read(self, obj):    
    #     return UserSerializer(instance=obj.usuario).data
    class Meta:
        model = Cliente
        fields = '__all__'
        
    # def create(self, validated_data):
    #     usuario_data = validated_data.pop('usuario')
    #     password = usuario_data.pop('password')
    #     usuario = User(**usuario_data)
    #     usuario.set_password(password)
    #     usuario.save()
    #     errors = {}
    #     try:
    #         cpf = validated_data.get('cpf')
    #         if Cliente.objects.filter(cpf=cpf).exists():
    #             errors.setdefault('cpf', []).append("Cliente com este CPF já existe.")
    #         username = usuario_data.get('username')
    #         if User.objects.filter(username=username).exists():
    #             errors.setdefault('usuario', {}).setdefault('username', []).append("Um usuário com este nome de usuário já existe.")
    #         email = validated_data.get('email')
    #         if Cliente.objects.filter(email=email).exists():
    #             errors.setdefault('email', []).append("Cliente com este email já está em uso.")
    #             return errors
    #     except:
    #         cliente = Cliente.objects.create(usuario=usuario, **validated_data)
    #     return cliente