from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from ..models import Cupom
from django.utils import timezone


@receiver(pre_save, sender=Cupom)
def marcar_expirado_cupom(sender, instance, **kwargs):
    if instance.validado_ate and instance.validado_ate < timezone.now():
        instance.marcar_expirado()


@receiver(post_save, sender=Cupom)
def marcar_valido_cupom(sender, instance, **kwargs):
    if instance.validado_ate and instance.validado_ate < timezone.now():
        instance.marcar_expirado()

@receiver(pre_save, sender=Cupom)
def cupom_pre_save(sender, instance, **kwargs):

    
    pre_save.disconnect(cupom_pre_save, sender=sender)
    
    obj = Cupom.objects.get(pk=instance.pk)
    if obj.validado_ate and instance.validado_ate and obj.validado_ate < instance.validado_ate and (instance.status_cupom=='Expirado' or instance.status_cupom=='Utilizado'):
        instance.revalidar()
    
    pre_save.connect(cupom_pre_save, sender=sender)