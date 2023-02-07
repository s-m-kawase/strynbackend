from rest_framework import serializers 
from core.models import Profile
from pedidos.api.serializers.restaurante_serializer import RestauranteSerializer


class ProfileSerializer(serializers.ModelSerializer):

    restaurante_read = serializers.SerializerMethodField()

    def get_restaurante_read(self, obj):    
        return RestauranteSerializer(instance=obj.restaurante).data


    class Meta:
        model = Profile
        fields = '__all__'