from django.db.models.signals import post_save
from django.dispatch import receiver
from crum import get_current_user
from ..models import Restaurante, Cardapio


@receiver(post_save, sender=Restaurante)
def adicionar_cardapio_ao_restaurante(sender, instance, created, **kwargs):
    '''Realiza ações após a model CategoriaCardapio ser salva.'''
    if created:
        Cardapio.objects.create(
            nome=f'Cardapio -{instance.nome}',
            restaurante=instance,
        )
