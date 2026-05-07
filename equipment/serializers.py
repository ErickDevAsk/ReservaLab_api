from rest_framework import serializers
from .models import Equipo, Incidencia

class EquipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipo
        fields = '__all__'

class IncidenciaSerializer(serializers.ModelSerializer):
    # Esto es para que en Angular podamos leer el nombre del equipo y no solo el ID número 3
    equipo_nombre = serializers.ReadOnlyField(source='equipo.nombre')
    
    class Meta:
        model = Incidencia
        fields = ['id', 'equipo', 'equipo_nombre', 'descripcion', 'fecha_reporte', 'estado']

