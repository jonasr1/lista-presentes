import secrets
from django.db import models
class Convidados(models.Model):
        status_choices = (
        ('AC', 'Aguardando confirmação'),
        ('C', 'Confirmado'),
        ('R', 'Recusado')
    )
        nome_convidado = models.CharField(max_length=100)
        whatsapp = models.CharField(max_length=25, null=True, blank=True)
        maximo_acompanhantes = models.PositiveIntegerField(default=0)
        acompanhantes_confirmados = models.PositiveIntegerField(default=0)
        token = models.CharField(max_length=25)
        status = models.CharField(max_length=2, choices=status_choices, default='AC')
        
        def save(self, *args, **kwargs): # type: ignore
            if not self.token:
                    self.token = secrets.token_urlsafe(16) # Gere um token único
            super(Convidados, self).save(*args, **kwargs)
        
        @property
        def link_convite(self):
            return f'http://127.0.0.1:8000/convidados/?token={self.token}'

        def __str__(self) -> str:
            return self.nome_convidado  

class Presentes(models.Model):
    nome_presente = models.CharField(("Nome do Presente"),max_length=100)
    foto = models.ImageField(("Foto"),upload_to='presentes')
    preco = models.DecimalField(("Preço"), max_digits=6, decimal_places=2)
    importancia = models.IntegerField(("Importância"))
    reservado = models.BooleanField(default=False)
    reservado_por = models.ForeignKey("Convidados", null=True, blank=True, on_delete=models.SET_NULL)
    
    class Meta:
        verbose_name='Presente'
        verbose_name_plural='Presentes'
    
    def __str__(self) -> str:
        return self.nome_presente
    
    @property
    def status_reserva(self) -> str:
        return f"Reservado por {self.reservado_por.nome_convidado}" if self.reservado_por else "Disponível"
    