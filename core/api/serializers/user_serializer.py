from rest_framework import serializers
from django.contrib.auth.models import User
from .profile_serializers import ProfileSerializer
class UserSerializer(serializers.ModelSerializer):

    profile = ProfileSerializer()
    
    class Meta:
        model = User
        fields = '__all__'