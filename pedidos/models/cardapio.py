from django.db import models
from pedidos.models.item_cardapio import ItemCardapio
from pedidos.models.categoria_cardapio import CategoriaCardapio
from pedidos.models.restaurante import Restaurante
from pedidos.models.grupo_complemento import GrupoComplementos


class Cardapio(models.Model):
    
    nome = models.CharField(
        max_length=100,
        verbose_name='Nome do cardapio',
        null=True,
        unique=True
    )

    categorias =  models.ManyToManyField(
        CategoriaCardapio,
        verbose_name='Categorias do Cardapio',
        blank=True, null=True
    )

    restaurante =  models.ForeignKey(
        Restaurante,
        on_delete=models.SET_NULL,
        verbose_name='Restaurante',
        null=True
    )
    
    grupo_complementos = models.ManyToManyField(
        GrupoComplementos,
        verbose_name='Grupo Complementos',
        blank=True, null=True
    )



    def __str__(self):
        return self.nome if self.nome else f'{self.id}'

    class Meta:
        app_label = 'pedidos'
        verbose_name = 'Cardapio'
        verbose_name_plural = 'Cardapios'
    

