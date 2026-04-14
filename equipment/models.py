from django.db import models
# Importamos el modelo Laboratorio para la llave foránea
from labs.models import Laboratorio 

class Equipo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    numero_inventario = models.CharField(max_length=50, unique=True)
    cantidad_total = models.PositiveIntegerField()
    cantidad_disponible = models.PositiveIntegerField()
    estado = models.CharField(max_length=20, default='Disponible')
    # Relación opcional: Un equipo puede pertenecer a un lab o ser general
    laboratorio = models.ForeignKey(Laboratorio, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} ({self.numero_inventario})"

def clean(self):
    if self.cantidad_disponible > self.cantidad_total:
        raise ValidationError("La cantidad disponible no puede ser mayor a la total")
    
    
def save(self, *args, **kwargs):
    if self.cantidad_disponible > self.cantidad_total:
        self.cantidad_disponible = self.cantidad_total
    super().save(*args, **kwargs)