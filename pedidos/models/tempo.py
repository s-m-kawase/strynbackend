from django.db import models


class TempoEstimado(models.Model):
    tempo = models.CharField(
        max_length=100,
        verbose_name="Tempo Estimado",
        blank=True, null=True,
    )

    def __str__(self):
        return self.tempo