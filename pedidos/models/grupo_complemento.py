from django.db import models
from pedidos.models.complemento import Complementos
from django.core.validators import MaxValueValidator, MinValueValidator


class GrupoComplementos(models.Model):

    nome = models.CharField(
        max_length=40,
        verbose_name='Nome do Grupo de Complementos',
        null=True,
        unique=True
    )

    obrigatoriedade = models.BooleanField(
        verbose_name='Obrigatorio ?',
        default=False
    )

    complemento = models.ManyToManyField(
        Complementos,
        verbose_name="Complementos",
        null=True
    )


    quantidade_minima = models.IntegerField(
        verbose_name="Quantidade Mínima",
        blank=True, null=True,
        validators = [MinValueValidator(1.0),MaxValueValidator(10.0)],
    )

    quantidade_maxima = models.IntegerField(
        verbose_name="Quantidade Máxima",
        blank=True, null=True,
        validators = [MinValueValidator(1.0),MaxValueValidator(10.0)],
    )


    def atualizar_catalogo(self, bool):
        pass

    def __str__(self):
        return self.nome if self.nome else f'{self.id}'

    class Meta:
        app_label = 'pedidos'
        verbose_name = 'Grupo Complemento'
        verbose_name_plural = 'Grupos Complementos'
    