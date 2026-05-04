from rest_framework import serializers
from datetime import datetime, timedelta
from labs.models import Laboratorio
from .models import Reserva

class CrearReservaSerializer(serializers.Serializer):
    # Ya no recibimos texto, ahora recibimos el ID numérico
    laboratorio = serializers.IntegerField() 
    fecha = serializers.DateField()
    hora_inicio = serializers.TimeField()
    duracion = serializers.IntegerField(min_value=1, max_value=4)
    equipo = serializers.CharField(required=False, allow_blank=True) 
    proposito = serializers.CharField(min_length=10)

    def validate(self, data):
        # 1. Verificar que el laboratorio exista en la BD (ahora buscando por 'id')
        try:
            lab = Laboratorio.objects.get(id=data['laboratorio'])
        except Laboratorio.DoesNotExist:
            raise serializers.ValidationError({"laboratorio": "El laboratorio ingresado no existe."})

        # 2. Calcular a qué hora termina la reserva
        fecha_hora_inicio = datetime.combine(data['fecha'], data['hora_inicio'])
        hora_fin_calculada = (fecha_hora_inicio + timedelta(hours=data['duracion'])).time()

        # 3. Validar Traslapes (La regla de oro)
        choques = Reserva.objects.filter(
            laboratorio=lab,
            fecha=data['fecha'],
            estado__in=['Pendiente', 'Aprobada'], 
            hora_inicio__lt=hora_fin_calculada, 
            hora_fin__gt=data['hora_inicio']    
        )

        if choques.exists():
            raise serializers.ValidationError("El laboratorio ya se encuentra reservado en este rango de horario.")

        # Pasamos datos extras validados a la vista
        data['laboratorio_obj'] = lab
        data['hora_fin'] = hora_fin_calculada
        
        return data