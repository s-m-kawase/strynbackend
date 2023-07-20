from django.db import models


class Destinatario(models.Model):
    '''
    Classe que serve para guardar o destinatário do email
    '''
    email = models.EmailField(
        verbose_name = 'Email'
    )

    def __str__(self):
        return self.email

    class Meta:
        app_label = 'emails'
        verbose_name = 'Destinatário'
        verbose_name_plural = 'Destinatários'
