from django.contrib import admin
from .models import Equipo

@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'numero_inventario', 'cantidad_disponible', 'estado')
    search_fields = ('nombre', 'numero_inventario')
