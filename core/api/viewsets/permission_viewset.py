import code
from os import name
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import JsonResponse
from django.contrib.auth.models import Permission
from ..serializers.permission_serializer import PermissionSerializer
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType


class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [filters.SearchFilter]

    search_fields = []

    # @action(detail=False, methods=["get"])
    # def solicitar_permissão(self, request):
    #     try:
    #         nome = self.request.GET.getlist("permission", [])
    #         grupo_acesso = self.request.GET.get("grupo", None)

    #         permissoes = Permission.objects.filter(codename__in=nome)
    #         grupo = GrupoAcesso.objects.get(id=grupo_acesso)
    #         grupo_admin = Group.objects.get(id=grupo.grupo_admin.id)

    #         grupo_admin.permissions.clear()

    #         grupo_admin.permissions.add(*permissoes)

    #         usuarios = grupo.participantes.all()

    #         for usuario in usuarios:
    #             usuario.groups.add(grupo_admin)

    #         return JsonResponse({"message": "permissions adicionada com sucesso"})

    #     except Permission.DoesNotExist:
    #         return JsonResponse({"message": "Permissão não encontrada"}, status=400)

    #     except GrupoAcesso.DoesNotExist:
    #         return JsonResponse(
    #             {"message": "Grupo de acesso não encontrado"}, status=400
    #         )

    #     except Group.DoesNotExist:
    #         return JsonResponse({"message": "Grupo não encontrado"}, status=400)

    #     except Exception as e:
    #         return JsonResponse({"message": f"Ocorreu um erro: {str(e)}"}, status=500)

    # def get_queryset(self):
    #     query = super().get_queryset()
    #     nome = self.request.query_params.get("nome", None)
    #     type = self.request.query_params.get("type", None)
    #     app = self.request.query_params.get("app", None)
    #     if nome:
    #         query = query.filter(name__icontains=nome)
    #     if app:
    #         content_types = ContentType.objects.filter(app_label=app)

    #         content_type_ids = content_types.values_list("id", flat=True)

    #         query = query.filter(content_type__in=content_type_ids)
    #     if type:
    #         query = query.filter(content_type=type)
    #     return query
