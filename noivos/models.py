from django.db import models

class Presentes(models.Model):
    nome_presente = models.CharField(("Nome do Presente"),max_length=100)
    foto = models.ImageField(("Foto"),upload_to='presentes')
    preco = models.DecimalField(("Preço"), max_digits=6, decimal_places=2)
    importancia = models.IntegerField(("Importância"))
    reservado = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return self.nome_presente
    