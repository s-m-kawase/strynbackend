from django.db.models.signals import pre_save
from django.dispatch import receiver
from ..models import Pedidos

@receiver(pre_save, sender=Pedidos)
def pedido_pre_save(sender, instance, **kwargs):

    
    pre_save.disconnect(pedido_pre_save, sender=sender)
    try:
        obj = Pedidos.objects.get(pk=instance.pk)
        if obj.status_pedido == 'Sacola' and instance.status_pedido == 'Aguardando Pagamento Mesa':
            instance.email_aguardando_pagamento_mesa()
    except:
        print("Error ao enviar email de aguardando pagamento de mesa")
    pre_save.connect(pedido_pre_save, sender=sender)