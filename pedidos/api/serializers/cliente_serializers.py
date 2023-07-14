from rest_framework import serializers
from core.models.profile import Profile 
from pedidos.models import Cliente
from core.api.serializers.user_serializer import UserSerializer
from django.contrib.auth.models import User


class ClienteSerializer(serializers.ModelSerializer):
    usuario = UserSerializer(write_only=True)


    # usuario_read = serializers.SerializerMethodField()

    # def get_usuario_read(self, obj):    
    #     return UserSerializer(instance=obj.usuario).data
    class Meta:
        model = Cliente
        fields = '__all__'
        
    def create(self, validated_data):
        usuario_data = validated_data.pop('usuario')
        password = usuario_data.pop('password')
        usuario = User(**usuario_data)
        usuario.set_password(password)
        usuario.save()

        cliente = Cliente.objects.create(usuario=usuario, **validated_data)
        return cliente
        