from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):

    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='Usuário',
        null=True
    )

    restaurante = models.ForeignKey(
        'pedidos.Restaurante',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def registrar(self):
        pass

    def login(self):
        pass

    def atualizar_perfil(self):
        pass

    def __str__(self) :
        return str(self.usuario)

    class Meta:
        app_label = 'core'
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
