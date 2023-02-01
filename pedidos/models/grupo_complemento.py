from django.db import models
from pedidos.models.complemento import Complementos
from django.core.validators import MaxValueValidator, MinValueValidator


class GrupoComplementos(models.Model):

    nome = models.CharField(
        max_length=40,
        verbose_name='Nome do Grupo de Complementos',
        blank=True, null=True,
    )

    obrigatoriedade = models.BooleanField(
        verbose_name='Obrigatorio ?',
        default=False
    )

    complemento = models.ManyToManyField(
        Complementos,
        verbose_name="Complementos",
        blank=True, null=True
    )


    quantidade = models.IntegerField(
        verbose_name="Quantidade de Complemento",
        blank=True, null=True,
        validators = [MinValueValidator(1.0),MaxValueValidator(10.0)],
    )


    def atualizar_catalogo(self, bool):
        pass

    def __str__(self):
        return self.nome

    class Meta:
        app_label = 'pedidos'
        verbose_name = 'Grupo Complemento'
        verbose_name_plural = 'Grupos Complementos'
    