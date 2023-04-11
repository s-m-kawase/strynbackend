from django.db.models.signals import post_save
from django.dispatch import receiver
from crum import get_current_user
from ..models import CategoriaCardapio, Cardapio


@receiver(post_save, sender=CategoriaCardapio)
def adicionar_categoria_ao_cardapio(sender, instance, created, **kwargs):
    '''Realiza ações após a model CategoriaCardapio ser salva.'''
    if created:
        usuario = get_current_user()
        cardapios = Cardapio.objects.filter(restaurante__usuario=usuario)
        for cardapio in cardapios:
            cardapio.categorias.add(instance)
        cardapio.save()
