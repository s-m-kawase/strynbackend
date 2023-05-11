from rest_framework import serializers 
from pedidos.models import Cliente
from core.api.serializers.user_serializer import UserSerializer


class ClienteSerializer(serializers.ModelSerializer):

    # usuario_read = serializers.SerializerMethodField()

    # def get_usuario_read(self, obj):    
    #     return UserSerializer(instance=obj.usuario).data
    class Meta:
        model = Cliente
        fields = '__all__'