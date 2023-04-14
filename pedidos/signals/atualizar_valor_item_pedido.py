from django.db.models.signals import post_save
from django.dispatch import receiver
from crum import get_current_user
from ..models import CategoriaCardapio, Cardapio, ItensPedido


@receiver(post_save, sender=ItensPedido)
def atualizar_valor_item_pedido(sender, instance, created, **kwargs):
    post_save.disconnect(atualizar_valor_item_pedido, sender=sender)
    instance.calcular_preco()
    post_save.connect(atualizar_valor_item_pedido, sender=sender)


