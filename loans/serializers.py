from rest_framework import serializers
from .models import Prestamo

class LoanSerializer(serializers.ModelSerializer):
    # Esto sigue igual: asigna el ID en la base de datos
    usuario = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    equipo_nombre = serializers.ReadOnlyField(source='equipo.nombre')
    
    usuario_nombre = serializers.ReadOnlyField(source='usuario.username') 

    class Meta:
        model = Prestamo
        fields = [
            'id', 
            'usuario', 
            'usuario_nombre', # <- Lo agregamos a la lista
            'equipo', 
            'equipo_nombre',  # <- Lo agregamos a la lista
            'cantidad_solicitada', 
            'fecha_prestamo', 
            'fecha_devolucion_prevista', 
            'estado'
        ]
        read_only_fields = ['id', 'fecha_prestamo']

