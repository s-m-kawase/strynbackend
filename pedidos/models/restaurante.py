from django.db import models


class Restaurante(models.Model):

    nome = models.CharField(
        max_length=90,
        verbose_name='Nome do Restaurante',
        blank=True, null=True,
    )

    descricao = models.TextField(
        max_length=1000,
        verbose_name="Descrição do Restaurante",
        blank=True, null=True,
    )

    logo = models.ImageField(
        verbose_name='Logo do Restaurante',
        blank=True, null=True,
        )

    total_mesa = models.IntegerField(
        verbose_name="Total de Mesas",
        blank=True, null=True,
    )

    horario_abertura = models.TimeField(
        verbose_name='Horario de Abertura',
        blank=True, null=True,
    )

    horario_encerramento = models.TimeField(
        verbose_name='Horario de Encerramento',
        blank=True, null=True,
    )

    def __str__(self):
        return self.nome

    class Meta:
        app_label = 'pedidos'
        verbose_name = 'Restaurante'
        verbose_name_plural = 'Restaurantes'
    