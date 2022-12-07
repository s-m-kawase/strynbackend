from django.db import models
from pedidos.models.categoria_cardapio import CategoriaCardapio
from pedidos.models.complemento import Complementos

class Item(models.Model):

    codigo_item = models.CharField(
        max_length=60,
        verbose_name='Codigo Item'
    )

    descricao = models.TextField(
        max_length=1000,
        verbose_name='Descrição do Item',
        blank=True, null=True,
    )

    preco = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Preço do Produto',
        blank=True, null=True,
    )

    status_venda = models.BooleanField(
        verbose_name='Está Pausado ?',
        default=False,
    )

    categoria = models.ForeignKey(
        CategoriaCardapio,
        on_delete=models.CASCADE,
        verbose_name='Categoria do Cardapio',
        blank=True, null=True,
    )
    
    tamanho_fome = (
        ('Nao se aplica','nao se aplica'),
        ('1 pessoa','uma pessoa'),
        ('2 pessoas','duas pessoas'),
        ('3 pessoas','tres pessoas'),
        ('4 pessoas','quatro pessoas'),
    )

    complemento = models.ForeignKey(
        Complementos,
        on_delete=models.CASCADE,
        verbose_name='Complementos',
        blank=True, null=True,
    )

    foto = models.ImageField(
        verbose_name='Foto',
        blank=True, null=True
    )


    def __str__(self):
         return str(self.codigo_item)
    
