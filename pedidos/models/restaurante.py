from django.db import models
from django.contrib.auth.models import User
from .tempo import TempoEstimado
from pedidos.models.categoria_cardapio import CategoriaCardapio

class Restaurante(models.Model):

    nome = models.CharField(
        max_length=90,
        verbose_name='Nome do Restaurante',
        null=True,
    )

    usuario = models.ManyToManyField(
        User,
        verbose_name='Usuários',
        blank=True, null=True
    )

    categoria = models.ForeignKey(
        CategoriaCardapio,
        on_delete=models.SET_NULL,
        verbose_name='Categoria do Cardapio',
        blank=True, null=True,
    )

    descricao = models.TextField(
        max_length=1000,
        verbose_name="Descrição do Restaurante",
        blank=True, null=True
    )

    logo = models.ImageField(
        verbose_name='Logo do Restaurante',
        blank=True, null=True,
    )

    baner = models.ImageField(
        verbose_name='Baner do Restaurante',
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
    tempo_estimado = models.ForeignKey(
        TempoEstimado,
        verbose_name='Tempo Estimado',
        on_delete=models.SET_NULL,
        blank=True, null=True,
    )


    taxa_servico = models.IntegerField(
        verbose_name="Taxa de serviço",
        blank=True, null=True,
        default=10
        )

    link_restaurante = models.TextField(
        verbose_name="Qr code Restaurante",
        null=True, blank=True,
    )

    def __str__(self):
        return self.nome

    class Meta:
        app_label = 'pedidos'
        verbose_name = 'Restaurante'
        verbose_name_plural = 'Restaurantes'
