from rest_framework import serializers
from django.contrib.auth.models import User
from .profile_serializers import ProfileSerializer
class UserSerializer(serializers.ModelSerializer):
    #profile = ProfileSerializer()

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
        fields = '__all__'