from rest_framework import viewsets, filters
import django_filters.rest_framework
from core.models import Profile
from ..serializers.profile_serializers import ProfileSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

class ProfileViewSet(viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    permission_classes = (IsAuthenticated,)
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    filter_backends = [filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]

    filterset_fields = ['restaurante']

    search_fields = ['restaurante']