__author__ = "Francisco Flávio Nogueira da Silva"
__copyright__ = "Copyright 2020, Flávio Silva"
__credits__ = ["Outbox Sistemas"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Francisco Flávio Nogueira da Silva"
__email__ = "flavio981895788@gmail.com"
__status__ = "Production"


from django.db import models


class Destinatario(models.Model):
    """
    Classe que serve para guardar o destinatário do email
    """
    email = models.EmailField(
        verbose_name = "Email"
    )

    def __str__(self):
        return self.email

    class Meta:
        app_label = "emails"
        verbose_name = "Destinatário"
        verbose_name_plural = "Destinatários"