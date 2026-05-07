from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from labs.models import Laboratorio
from loans.models import Prestamo
from reservations.models import Reserva
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

class AdminDashboardView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        hoy = timezone.now().date()
        
        # --- 1. Contadores Globales ---
        total_usuarios = User.objects.count()
        
        # Ajusta 'rol' al nombre de tu campo (ej: role, tipo_usuario, is_staff)
        tecnicos_activos = User.objects.filter(rol=2).count() 
        
        laboratorios_red = Laboratorio.objects.count()
        
        # Ajusta 'fecha' al nombre de tu campo en Reserva (ej: fecha_reserva, inicio)
        reservas_hoy = Reserva.objects.filter(fecha=hoy).count()

        # --- 2. Gráfica de Pastel: Estado de Reservas ---
        # Ajusta los textos ('Confirmada', etc.) a las opciones (choices) de tu modelo
        datos_estado = [
            {"name": "Confirmadas", "value": Reserva.objects.filter(estado='Confirmada').count()},
            {"name": "Pendientes", "value": Reserva.objects.filter(estado='Pendiente').count()},
            {"name": "Canceladas", "value": Reserva.objects.filter(estado='Cancelada').count()},
            {"name": "Finalizadas", "value": Reserva.objects.filter(estado='Finalizada').count()},
        ]

        # --- 3. Gráfica de Línea: Tendencia 7 días ---
        tendencia_series = []
        dias_semana = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]

        for i in range(6, -1, -1):
            fecha_evaluar = hoy - timedelta(days=i)
            cantidad = Reserva.objects.filter(fecha=fecha_evaluar).count()
            nombre_dia = dias_semana[fecha_evaluar.weekday()]
            
            tendencia_series.append({
                "name": f"{nombre_dia} {fecha_evaluar.day}", # Ej: "Lun 4"
                "value": cantidad
            })

        datos_tendencia = [{
            "name": "Reservas",
            "series": tendencia_series
        }]

        # --- 4. Retornar el JSON ---
        return Response({
            'totalUsuarios': total_usuarios,
            'tecnicosActivos': tecnicos_activos,
            'laboratoriosRed': laboratorios_red,
            'reservasHoy': reservas_hoy,
            'datosEstado': datos_estado,
            'datosTendencia': datos_tendencia
        })
    
class TecnicoDashboardView(APIView):
    permission_classes = [IsAuthenticated]