from django.db import models
from django.conf import settings
from equipment.models import Equipo

class Prestamo(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    cantidad_solicitada = models.PositiveIntegerField()
    fecha_prestamo = models.DateTimeField(auto_now_add=True) # Se guarda automático al crear
    fecha_devolucion_prevista = models.DateTimeField()
    fecha_devolucion_real = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=20, default='En curso') # En curso, Devuelto, Con Incidencia

    def __str__(self):
        return f"Prestamo {self.equipo} - {self.usuario}"

class Incidencia(models.Model):
    prestamo = models.OneToOneField(Prestamo, on_delete=models.CASCADE)
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE) # Redundante pero útil para reportes rápidos
    descripcion_danio = models.TextField()
    fecha_reporte = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Incidencia: {self.equipo.nombre}"

