from rest_framework import generics, serializers, viewsets
from core.models import Profile
from ..serializers.profile_serializers import ProfileSerializer

from rest_framework.permissions import IsAuthenticated


class ProfileViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer