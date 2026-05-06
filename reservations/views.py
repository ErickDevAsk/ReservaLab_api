from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from accounts.permissions import IsAdminOrTecnico
from .serializers import CrearReservaSerializer
from .models import Reserva
from django.db.models import Q

class CrearReservaView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CrearReservaSerializer(data=request.data)
        
        if serializer.is_valid():
            datos = serializer.validated_data
            
            # --- NUEVA LÓGICA DE VALIDACIÓN DE DISPONIBILIDAD ---
            # Verificamos si ya existe una reserva aprobada que choque con este horario
            choque_horario = Reserva.objects.filter(
                laboratorio=datos['laboratorio_obj'],
                fecha=datos['fecha'],
                estado='Aprobada' # Solo nos importan las que ya están confirmadas
            ).filter(
                # Lógica de traslape: (InicioA < FinB) Y (FinA > InicioB)
                Q(hora_inicio__lt=datos['hora_fin'], hora_fin__gt=datos['hora_inicio'])
            ).exists()

            if choque_horario:
                return Response({
                    "error": "El laboratorio ya se encuentra ocupado en ese horario. Por favor elige otro."
                }, status=status.HTTP_400_BAD_REQUEST)

            # --- AUTO-APROBACIÓN ---
            nueva_reserva = Reserva.objects.create(
                usuario=request.user,
                laboratorio=datos['laboratorio_obj'],
                fecha=datos['fecha'],
                hora_inicio=datos['hora_inicio'],
                hora_fin=datos['hora_fin'],
                motivo=datos['proposito'],
                estado='Aprobada'
            )
            
            return Response({
                "mensaje": "¡Reserva confirmada exitosamente!",
                "reserva_id": nueva_reserva.id,
                "estado": nueva_reserva.estado
            }, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class ListarReservasPorLaboratorioView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, laboratorio_id):
        # Ahora solo filtramos por 'Aprobada' ya que no habrá 'Pendientes' nuevas
        reservas = Reserva.objects.filter(
            laboratorio_id=laboratorio_id,
            estado='Aprobada'
        )
        
        data = []
        for r in reservas:
            data.append({
                "id": r.id,
                "fecha": str(r.fecha),
                "hora_inicio": str(r.hora_inicio),
                "hora_fin": str(r.hora_fin),
                "estado": r.estado,
                "usuario": r.usuario.username # Agregado por si se quiere saber quién ocupó el lugar
            })
            
        return Response(data, status=status.HTTP_200_OK)
    
# ==========================================
# ENDPOINT PARA RECHAZAR RESERVA
# ==========================================
class RechazarReservaView(APIView):
    # ¡Candado puesto!
    permission_classes = [IsAdminOrTecnico]

    def patch(self, request, pk):
        reserva = get_object_or_404(Reserva, pk=pk)
        
        reserva.estado = 'Rechazada'
        reserva.save()
        
        return Response({
            "mensaje": f"La reserva de {reserva.usuario.username} ha sido RECHAZADA.",
            "estado": reserva.estado
        }, status=status.HTTP_200_OK)
    
class AprobarReservaView(APIView):
    # ¡Candado puesto! Solo Admin o Técnicos pueden aprobar
    permission_classes = [IsAdminOrTecnico]

    def patch(self, request, pk):
        # Buscamos la reserva en la base de datos (si no existe, lanza error 404 automático)
        reserva = get_object_or_404(Reserva, pk=pk)
        
        # Cambiamos el estado y guardamos
        reserva.estado = 'Aprobada'
        reserva.save()
        
        return Response({
            "mensaje": f"La reserva de {reserva.usuario.username} ha sido APROBADA.",
            "estado": reserva.estado
        }, status=status.HTTP_200_OK)

class MisReservasView(APIView):
    permission_classes = [IsAuthenticated] # Solo usuarios logueados

    def get(self, request):
        # Filtramos por el usuario que está haciendo la petición
        # Y las ordenamos por fecha más reciente
        reservas = Reserva.objects.filter(usuario=request.user).order_by('-fecha', '-hora_inicio')
        
        data = []
        for r in reservas:
            data.append({
                "id": r.id,
                # Intentamos sacar el nombre del lab, si no, mandamos su ID
                "laboratorio": getattr(r.laboratorio, 'nombre', r.laboratorio_id), 
                "fecha": str(r.fecha),
                "hora_inicio": str(r.hora_inicio),
                "hora_fin": str(r.hora_fin),
                "motivo": r.motivo,
                "estado": r.estado
            })
            
        return Response(data, status=status.HTTP_200_OK)
    
