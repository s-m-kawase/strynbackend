from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Nome de Usuario',
        )

    email = models.EmailField(
        verbose_name='E-mail do Usuario'
    )

    senha = models.CharField(
        max_length=100,
        verbose_name='Senha',
    )

    data_registro = models.DateField(
        verbose_name='Data do Registro',
        auto_now=True,
    )


    def registrar(self):
        pass

    def login(self):
        pass

    def atualizar_perfil(self):
        pass

    #def __str__(self) :
    #    return self
