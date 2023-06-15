""" from django.db.models.signals import post_save
from django.dispatch import receiver
from ..models import Pedidos
import requests


@receiver(post_save, sender=Pedidos)
def criar_pagamento(sender, instance, created, **kwargs):
    post_save.disconnect(criar_pagamento, sender=sender)
    if created:

        if instance.payment_intent_id:
            instance.pagamento = 'Pagamento online'
            instance.valor_pago = instance.total
            instance.pedido = instance.id
        else:
            instance.pagamento = 'Pagamento na mesa'
            instance.valor_pago = instance.total
            instance.pedido = instance.id

    instance.save()
    post_save.connect(criar_pagamento, sender=sender) """