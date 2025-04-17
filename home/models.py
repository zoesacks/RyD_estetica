from django.db import models

# Create your models here.
from django.db import models

class Servicio(models.Model):
    CATEGORIAS = [
        ('facial', 'Facial'),
        ('corporal', 'Corporal'),
        # Podés agregar más si querés
    ]

    categoria = models.CharField(max_length=50, choices=CATEGORIAS)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    beneficio_uno = models.CharField(max_length=255, blank=True, null=True)
    beneficio_dos = models.CharField(max_length=255, blank=True, null=True)
    beneficio_tres = models.CharField(max_length=255, blank=True, null=True)
    imagen = models.ImageField(upload_to='servicios/')
    duracion = models.CharField(max_length=50, help_text="Ej: 60 minutos")
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def obtener_beneficios(self):
        return [b for b in [self.beneficio_uno, self.beneficio_dos, self.beneficio_tres] if b]

    def __str__(self):
        return self.titulo
