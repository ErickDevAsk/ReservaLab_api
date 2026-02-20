from django.contrib import admin
from .models import Laboratorio

@admin.register(Laboratorio)
class LaboratorioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'edificio', 'capacidad', 'estado') # Lo que verás en la lista
    list_filter = ('edificio', 'estado') # Filtros laterales
