from django.db import models


class TempoEstimado(models.Model):
    tempo = models.CharField(
        max_length=100,
        verbose_name="Tempo Estimado",
        blank=True, null=True,
    )

    def __str__(self):
        return self.tempo

    class Meta:
        app_label = 'pedidos'
        verbose_name = 'Tempo Estimado'
        verbose_name_plural = 'Tempo Estimados'
