from django.db import models

class Laboratorio(models.Model):
    nombre = models.CharField(max_length=100)
    edificio = models.CharField(max_length=50)
    piso = models.CharField(max_length=20)
    capacidad = models.PositiveIntegerField()
    tipo = models.CharField(max_length=50)  # Cómputo, Electrónica
    estado = models.CharField(max_length=20, default='Activo')  # Activo, Mantenimiento
    facultad = models.CharField(max_length=50, default='FCC') 
    imagen = models.URLField(max_length=500, blank=True, null=True) 
    def __str__(self):
        return f"{self.nombre} ({self.edificio})"
