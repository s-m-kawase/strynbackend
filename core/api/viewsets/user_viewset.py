from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from ..serializers.user_serializer import UserSerializer
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.http.response import JsonResponse
from django.contrib.auth.models import User



class UserViewSet(ModelViewSet):
    authentication_classes = (SessionAuthentication, JWTAuthentication)
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filterset_fields = ('id',)

    @action(methods=['get'], detail=False)
    def usuario_logado(self, request):
        dic = UserSerializer(request.user, read_only=True)
        return JsonResponse(dic.data, content_type="application/json", safe=False)
