from django.db import models
from core.models.profile import Profile
from django.contrib.auth.models import User

class Cliente(models.Model):

    usuario = models.OneToOneField(
        User,
        verbose_name="Usuário",
        on_delete=models.SET_NULL,
        null=True
    )

    nome_cliente = models.CharField(
        verbose_name='Nome do Cliente',
        max_length=200,
        null=True
    )

    cpf = models.CharField(
        verbose_name="CPF",
        max_length=14,
        unique=True,
        null=True,
        blank=True
    )

    celular = models.CharField(
        verbose_name="Numero Celular",
        max_length=17,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.nome_cliente

    class Meta:
        app_label = 'pedidos'
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

