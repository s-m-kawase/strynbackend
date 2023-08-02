from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from ..serializers.user_serializer import UserSerializer
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.http.response import JsonResponse
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


class UserViewSet(ModelViewSet):
    pagination_class = StandardResultsSetPagination
    authentication_classes = (SessionAuthentication, JWTAuthentication)
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filterset_fields = ('id',)

    @action(methods=['get'], detail=False)
    def usuario_logado(self, request):
        dic = UserSerializer(request.user, read_only=True)
        return JsonResponse(dic.data, content_type="application/json", safe=False)

    
