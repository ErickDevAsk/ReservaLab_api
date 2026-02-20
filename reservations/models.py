from django.db import models
from django.conf import settings
from labs.models import Laboratorio

class Reserva(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    laboratorio = models.ForeignKey(Laboratorio, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    motivo = models.TextField()
    estado = models.CharField(max_length=20, default='Pendiente') # Pendiente, Aprobada, Rechazada

    def __str__(self):
        return f"Reserva {self.laboratorio} - {self.fecha}"