from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import CrearReservaSerializer
from .models import Reserva

class CrearReservaView(APIView):
    # Esto asegura que solo usuarios con token puedan hacer la petición
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CrearReservaSerializer(data=request.data)
        
        if serializer.is_valid():
            datos = serializer.validated_data
            
            # Guardamos la reserva usando los datos mapeados
            nueva_reserva = Reserva.objects.create(
                usuario=request.user, # Sacamos el ID del usuario del token
                laboratorio=datos['laboratorio_obj'],
                fecha=datos['fecha'],
                hora_inicio=datos['hora_inicio'],
                hora_fin=datos['hora_fin'],
                motivo=datos['proposito'], # El JSON manda "proposito", la BD usa "motivo"
                estado='Pendiente'
            )
            
            # TODO: Cuando creen el modelo ReservaEquipo, aquí se guardaría el equipo

            return Response({
                "mensaje": "Reserva solicitada con éxito.",
                "reserva_id": nueva_reserva.id
            }, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)