from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from ..models import ItensPedidoComplementos, ItensPedido
from .atualizar_valor_item_pedido import atualizar_valor_item_pedido


@receiver(post_delete, sender=ItensPedidoComplementos)
def autalizar_delete_complemento(sender, instance, **kwargs):
    post_delete.disconnect(atualizar_valor_item_pedido, sender=sender)
    try:
        instance.item_pedido.calcular_preco_item_mais_complementos()
    except:
        pass
    post_delete.connect(atualizar_valor_item_pedido, sender=sender)


