from django.db import models

from noivos.models import Convidados

class Acompanhante(models.Model):
    nome = models.CharField(max_length=100)
    convidado = models.ForeignKey(Convidados, on_delete=models.CASCADE, related_name='acompanhantes')

    def __str__(self):
        return self.nome