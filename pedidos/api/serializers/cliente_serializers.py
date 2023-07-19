from rest_framework import serializers
from core.models.profile import Profile 
from pedidos.models import Cliente
from core.api.serializers.user_serializer import UserSerializer
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class ClienteSerializer(serializers.ModelSerializer):
    usuario = UserSerializer(write_only=True)


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