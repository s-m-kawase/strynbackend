from django.db.models.signals import post_save
from django.dispatch import receiver
from ..models import ItensPedidoComplementos, ItensPedido
from .atualizar_valor_item_pedido import atualizar_valor_item_pedido


@receiver(post_save, sender=ItensPedidoComplementos)
def atualizar_valor_complemento_no_pedido(sender, instance, created, **kwargs):
    post_save.disconnect(atualizar_valor_complemento_no_pedido, sender=sender)
    post_save.disconnect(atualizar_valor_item_pedido, sender=ItensPedido)
    instance.item_pedido.calcular_preco()
    post_save.connect(atualizar_valor_item_pedido, sender=ItensPedido)
    post_save.connect(atualizar_valor_complemento_no_pedido, sender=sender)


