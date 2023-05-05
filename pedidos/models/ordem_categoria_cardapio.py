from django.db import models
from .cardapio import Cardapio
from .categoria_cardapio import CategoriaCardapio


class OrdemCategoriaCardapio(models.Model):

    cardapio = models.ForeignKey(
        Cardapio,
        verbose_name="Cardapio",
        on_delete=models.CASCADE,
        null=True, blank=True
        )
    
    categoria = models.ForeignKey(
        CategoriaCardapio,
        verbose_name="Categoria",
        on_delete=models.CASCADE,
        null=True, blank=True
        )

    ordem = models.IntegerField(
        verbose_name="Ordem",
        null=True, blank=True
        )


    

    def __str__(self):
        '''Método que retorna a representação do objeto como string.'''
        return str(self.id)

    class Meta:
        '''Sub classe para definir meta atributos da classe principal.'''

        app_label = 'pedidos'
        verbose_name = 'Ordem categoria Cardapio'
        verbose_name_plural = 'Ordem categorias cardapios'
