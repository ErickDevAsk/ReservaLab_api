from django.db import models
from django.contrib.auth.models import AbstractUser

class Rol(models.Model):
    nombre_rol = models.CharField(max_length=50, unique=True)  # Admin, Tecnico, Estudiante

    def __str__(self):
        return self.nombre_rol

class Usuario(AbstractUser):
    # Heredamos de AbstractUser, así que ya tiene username, password, first_name, email, etc.
    matricula_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    carrera_departamento = models.CharField(max_length=100, null=True, blank=True)
    rol = models.ForeignKey(Rol, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return f"{self.username} - {self.matricula_id}"
