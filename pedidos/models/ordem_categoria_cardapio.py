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


    def save(self, *args, **kwargs):
        if not self.ordem and self.cardapio: # verifica se o valor da ordem já foi definido
            last_order = OrdemCategoriaCardapio.objects.filter(cardapio=self.cardapio).order_by('-ordem').first()
            if last_order:
                self.ordem = last_order.ordem + 1
            else:
                self.ordem = 1
        super().save(*args, **kwargs)

    def __str__(self):
        '''Método que retorna a representação do objeto como string.'''
        return str(self.id)

    class Meta:
        '''Sub classe para definir meta atributos da classe principal.'''

        app_label = 'pedidos'
        verbose_name = 'Ordem categoria Cardapio'
        verbose_name_plural = 'Ordem categorias cardapios'
