from rest_framework import viewsets, status
from .models import Equipo
from .serializers import EquipoSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
# nuestro cadenero desde accounts
from accounts.permissions import IsAdminOrTecnico 
from .models import Incidencia
from .serializers import IncidenciaSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

class EquipoViewSet(viewsets.ModelViewSet):
    queryset = Equipo.objects.all()
    serializer_class = EquipoSerializer
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAdminOrTecnico()]
    
class IncidenciaAPIView(APIView):
    # ¡Candado puesto! Solo Técnicos y Admins pueden gestionar esto
    permission_classes = [IsAdminOrTecnico]

    def get(self, request):
        # Traemos solo las incidencias activas para el Dashboard
        # Las ordenamos de la más reciente a la más antigua
        incidencias = Incidencia.objects.filter(
            estado__in=['Pendiente', 'En Reparacion']
        ).order_by('-fecha_reporte')
        
        serializer = IncidenciaSerializer(incidencias, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # Recibimos el reporte de daño desde Angular y lo guardamos
        serializer = IncidenciaSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                "mensaje": "Incidencia registrada correctamente. El equipo requiere revisión.",
                "incidencia": serializer.data
            }, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResolverIncidenciaAPIView(APIView):
    permission_classes = [IsAdminOrTecnico] # Reutilizamos tu permiso

    def post(self, request, pk):
        # Buscamos la incidencia por su ID
        incidencia = get_object_or_404(Incidencia, pk=pk)

        if incidencia.estado != 'Resuelta':
            # 1. Cambiamos el estado a Resuelta
            incidencia.estado = 'Resuelta'
            incidencia.save()

            # 2. Le sumamos +1 al stock disponible de ese equipo
            equipo = incidencia.equipo
            if equipo.cantidad_disponible < equipo.cantidad_total:
                equipo.cantidad_disponible += 1
                equipo.save()

            return Response({"mensaje": "Equipo liberado exitosamente."}, status=status.HTTP_200_OK)
            
        return Response({"error": "Esta incidencia ya estaba resuelta."}, status=status.HTTP_400_BAD_REQUEST)
