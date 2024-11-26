from django.db import models
from django.contrib.auth.models import User


class CategoriaCardapio(models.Model):

    nome = models.CharField(
        max_length=40,
        verbose_name='Nome da Categoria',
        null=True,
    )

    status = models.BooleanField(
        verbose_name='Está pausado ?',
        default=False
    )

    em_promocao = models.BooleanField(
        default=False,
        verbose_name='Em promoção ?'
    )

    usuario_criacao = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name='Usuário de criação',
        blank=True,
        null=True,
    )

    ordem = models.IntegerField(
        verbose_name='Ordem',
        default=0,
    )
    
    

    
    def usuario_logado(self, request):
        return self.request.user
    
    def save(self, *args, **kwargs):
        if self.em_promocao is None:
            self.em_promocao = False
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome    if self.nome else f'{self.id}'

    class Meta:
        app_label = 'pedidos'
        verbose_name = 'Categoria Cardapio'
        verbose_name_plural = 'Categorias Cardapios'
    