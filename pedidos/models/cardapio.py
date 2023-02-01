from django.db import models
from pedidos.models.item_cardapio import ItemCardapio
from pedidos.models.categoria_cardapio import CategoriaCardapio
from pedidos.models.restaurante import Restaurante


class Cardapio(models.Model):
    
    nome = models.CharField(
        max_length=100,
        verbose_name='Nome do cardapio',
        blank=True, null=True,
        )

    itens = models.ManyToManyField(
            ItemCardapio,
            verbose_name='Itens Para Cardapio',
            blank=True, null=True,
        )

    categorias =  models.ManyToManyField(
            CategoriaCardapio,
            verbose_name='Categoria do Cardapio',
            blank=True, null=True,
        )

    restaurante =  models.ForeignKey(
            Restaurante,
            on_delete=models.Case,
            verbose_name='Nome do Restaurante',
            blank=True, null=True,
        )



    def __str__(self):
        return self.nome

    class Meta:
        app_label = 'pedidos'
        verbose_name = 'Cardapio'
        verbose_name_plural = 'Cardapios'
    

