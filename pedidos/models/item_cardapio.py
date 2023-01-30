from django.db import models
from pedidos.models.categoria_cardapio import CategoriaCardapio
from pedidos.models.grupo_complemento import GrupoComplementos


class ItemCardapio(models.Model):

    codigo_item = models.CharField(
        max_length=60,
        verbose_name='Codigo Item'
    )

    nome = models.TextField(
        max_length=100,
        verbose_name="Nome do Item",
        blank=True, null=True
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
    
    CHOICE_FOME = (
        ('Nao se aplica','nao se aplica'),
        ('1 pessoa','uma pessoa'),
        ('2 pessoas','duas pessoas'),
        ('3 pessoas','tres pessoas'),
        ('4 pessoas','quatro pessoas'),
    )

    tamanho_fome = models.CharField(
        verbose_name="Tamanho Fome",
        choices=CHOICE_FOME,
        max_length=50
    )


    grupo_complemento = models.ForeignKey(
        GrupoComplementos,
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
    
