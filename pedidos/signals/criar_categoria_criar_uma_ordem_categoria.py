from django.db.models.signals import post_save
from django.dispatch import receiver
from pedidos.models import CategoriaCardapio, Cardapio, OrdemCategoriaCardapio
from pedidos.models.ordem_categoria_cardapio import OrdemCategoriaCardapio


@receiver(post_save, sender=CategoriaCardapio)
def criar_ordem_categoria_cardapio(sender, instance, created, **kwargs):
    if created:
        cardapios = Cardapio.objects.all()
        for cardapio in cardapios:
            ordem_existe = OrdemCategoriaCardapio.objects.filter(categoria=instance, cardapio=cardapio).exists()
            if not ordem_existe:
                ordem = OrdemCategoriaCardapio.objects.create(categoria=instance, cardapio=cardapio)
                ordem.save()


# @receiver(post_save, sender=Cardapio)
# def criar_ordem_categoria_cardapio2(sender, instance, created, **kwargs):
#     if created:
#         categorias = CategoriaCardapio.objects.all()
        
#         for categoria in categorias:
#             ordem_existe = OrdemCategoriaCardapio.objects.filter(categoria=categoria, cardapio=instance).exists()
#             if not ordem_existe:
#                 ordem = OrdemCategoriaCardapio.objects.create(categoria=categoria, cardapio=instance)
#                 ordem.save()


@receiver(post_save, sender=OrdemCategoriaCardapio)
def criar_ordem_categoria_cardapio3(sender, instance, created, **kwargs):
    if created:
        if not instance.ordem and instance.cardapio: # verifica se o valor da ordem já foi definido
            last_order = OrdemCategoriaCardapio.objects.filter(cardapio=instance.cardapio).exclude(id=instance.id).order_by('-ordem').first()          
            try:
                instance.ordem = last_order.ordem + 1
            except:
                instance.ordem = 0
        

