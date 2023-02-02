from django.db import models
from pedidos.models.categoria_cardapio import CategoriaCardapio
from pedidos.models.grupo_complemento import GrupoComplementos


class ItemCardapio(models.Model):

    nome = models.CharField(
        max_length=100,
        verbose_name="Nome do Item",
        blank=False, null=True
    )
    
    descricao = models.TextField(
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

    categoria = models.ManyToManyField(
        CategoriaCardapio,
        verbose_name='Categoria do Cardapio',
        blank=False, null=False,
    )
    
    CHOICE_FOME = (
        ('Nao se aplica','Nãoo se aplica'),
        ('1 pessoa','1 pessoa'),
        ('2 pessoas','2 pessoas'),
        ('3 pessoas','3 pessoas'),
        ('4 pessoas','4 pessoas'),
    )

    tamanho_fome = models.CharField(
        verbose_name="Tamanho Fome",
        choices=CHOICE_FOME,
        max_length=50
    )

    grupo_complemento = models.ManyToManyField(
        GrupoComplementos,
        verbose_name='Complementos',
        blank=False, null=False,
    )
    

    foto = models.ImageField(
        verbose_name='Foto',
        blank=True, null=True
    )


    def __str__(self):
        return str(self.nome)

    class Meta:
        app_label = 'pedidos'
        verbose_name = 'Item cardapio'
        verbose_name_plural = 'Itens Cardapios'    
    
