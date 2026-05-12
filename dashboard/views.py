from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models import Sum, Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from labs.models import Laboratorio
from loans.models import Prestamo
from reservations.models import Reserva
from datetime import timedelta
from equipment.models import Incidencia, Equipo


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
    
    def get(self, request):
        hoy = timezone.now().date()
        # --- 1. Alertas de dispositivos dañados ---
        # Buscamos las incidencias que no se han resuelto
        # El [:5] es para traer solo las 5 más recientes y no saturar la cajita
        incidencias = Incidencia.objects.filter(
            estado__in=['Pendiente', 'En Reparacion']
        ).order_by('-fecha_reporte')[:5]

        alertas_danos = []
        for inc in incidencias:
            alertas_danos.append({
                "id": inc.id,
                "equipo_nombre": inc.equipo.nombre,
                "descripcion": inc.descripcion,
                "estado": inc.estado,
                # Formateamos la fecha para que Angular la lea bonito
                "fecha": inc.fecha_reporte.strftime("%Y-%m-%d %H:%M") 
            })

        # --- 2. Retornar el JSON ---
        # Aquí después puedes agregar más cosas si el dashboard del técnico pide 
        # "préstamos de hoy" o algo así, por ahora mandamos las alertas.
        prestamos_activos = Prestamo.objects.filter(estado='Aprobado    ').order_by('fecha_devolucion_prevista')[:5]

        lista_devoluciones = []
        for p in prestamos_activos:
            # Extraemos solo la fecha (sin la hora) para comparar
            fecha_dev = p.fecha_devolucion_prevista.date() if hasattr(p.fecha_devolucion_prevista, 'date') else p.fecha_devolucion_prevista

            # Lógica de los colores/estados
            if fecha_dev < hoy:
                estado_tag = 'Vencido'
            elif fecha_dev <= hoy + timedelta(days=2):
                estado_tag = 'Vence pronto'
            else:
                estado_tag = 'Vigente'

            # Intentamos sacar el nombre completo, si no, usamos el username
            nombre_estudiante = p.usuario.get_full_name() if p.usuario.get_full_name() else p.usuario.username

            lista_devoluciones.append({
                "id": p.id,
                "estudiante": nombre_estudiante,
                "equipo": p.equipo.nombre,
                "codigo": p.equipo.numero_inventario,
                "fecha": p.fecha_devolucion_prevista.strftime("%d/%m/%Y"),
                "estado": estado_tag
            })

                # --- 4. Datos para Gráficas (ngx-charts format) ---
        ocupacion_semanal = [
            {"name": "Lun", "value": 75},
            {"name": "Mar", "value": 82},
            {"name": "Mié", "value": 68},
            {"name": "Jue", "value": 90},
            {"name": "Vie", "value": 85},
            {"name": "Sáb", "value": 45},
            {"name": "Dom", "value": 30},
        ]

        tendencia_reservas = [{
            "name": "Reservas",
            "series": [
                {"name": "Ene", "value": 20},
                {"name": "Feb", "value": 35},
                {"name": "Mar", "value": 40},
                {"name": "Abr", "value": 50},
                {"name": "May", "value": 65},
                {"name": "Jun", "value": 80},
            ]
        }]

        # --- 5. Contadores Superiores (KPIs) ---
        
        # 1. Reservas Hoy
        reservas_hoy_count = Reserva.objects.filter(fecha=hoy).count()

        # 2. Equipos Disponibles (Sumamos la cantidad_disponible de todos los equipos)
        # Usamos 'or 0' por si la base de datos está vacía y devuelve None
        suma_equipos = Equipo.objects.aggregate(total=Sum('cantidad_disponible'))['total'] or 0

        # 3. Devoluciones Pendientes (Usamos la variable que ya filtraste arriba para la tabla)
        # Nota: asegúrate de usar la variable donde hiciste el .filter() de los préstamos
        devoluciones_count = prestamos_activos.count()

        # 4. Equipos en Mantenimiento (Contamos las incidencias que no están resueltas)
        mantenimiento_count = Incidencia.objects.filter(estado__in=['Pendiente', 'En Reparacion']).count()

        # --- 3. Retornamos todo junto ---
        return Response({
            'alertas_danos': alertas_danos,
            'devoluciones_pendientes': lista_devoluciones,
            'ocupacion_semanal': ocupacion_semanal,
            'tendencia_reservas': tendencia_reservas,
            'reservas_hoy': reservas_hoy_count,
            'equipos_disponibles': suma_equipos,
            'total_devoluciones': devoluciones_count,
            'equipos_mantenimiento': mantenimiento_count
        })

class TecnicoReportesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        hoy = timezone.now()
        # Obtenemos el primer día del mes actual para calcular "Nuevos usuarios"
        inicio_mes = hoy.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        # --- 1. KPIs (Tarjetas Superiores) ---
        total_prestamos = Prestamo.objects.count()
        
        # Ajusta 'date_joined' si el campo de fecha de registro de tu User se llama diferente
        nuevos_usuarios = User.objects.filter(date_joined__gte=inicio_mes).count()
        
        # Ajusta 'Confirmada' al estado que uses en tu modelo Reserva
        reservas_activas = Reserva.objects.filter(estado='Confirmada').count()

        # Cálculo de Tasa de Ocupación
        total_equipos = Equipo.objects.aggregate(total=Sum('cantidad_total'))['total'] or 1
        equipos_en_uso = Prestamo.objects.filter(estado='Activo').count()
        tasa_ocupacion = round((equipos_en_uso / total_equipos) * 100) if total_equipos > 0 else 0

        # --- 2. Datos para Gráficas ---
        
        # A) Gráfica de Dona: Top Equipos o Categorías
        # Agrupamos los préstamos para ver qué es lo que más se pide.
        # *Nota: Si tu modelo Equipo tiene categoría, puedes cambiar 'equipo__nombre' por 'equipo__categoria__nombre'
        distribucion = Prestamo.objects.values('equipo__nombre').annotate(total=Count('id')).order_by('-total')[:5]
        
        pie_chart_data = []
        for item in distribucion:
            pie_chart_data.append({
                "name": item['equipo__nombre'], 
                "value": item['total']
            })
            
        # Si la base de datos está vacía, mandamos un valor por defecto para que la dona no desaparezca
        if not pie_chart_data:
            pie_chart_data = [{"name": "Aún sin préstamos", "value": 1}]

        # B) Gráficas de Línea y Barras: Tendencia de los últimos 7 días
        line_series = []
        bar_chart_data = []
        dias_semana = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
        
        for i in range(6, -1, -1):
            fecha_evaluar = hoy.date() - timedelta(days=i)
            nombre_dia = dias_semana[fecha_evaluar.weekday()]
            
            # 1. Contamos las reservas de ese día (usando tu campo 'fecha' de Reserva)
            cant_reservas = Reserva.objects.filter(fecha=fecha_evaluar).count()
            
            # 2. Contamos los préstamos. 
            # ⚠️ IMPORTANTE: Ajusta 'fecha_devolucion_prevista' al campo donde guardas cuándo se hizo el préstamo (ej. 'fecha_prestamo' o 'fecha_inicio')
            cant_prestamos = Prestamo.objects.filter(fecha_devolucion_prevista__date=fecha_evaluar).count() 
            
            # Armamos la línea (Tendencia Mensual / Semanal)
            line_series.append({
                "name": f"{nombre_dia} {fecha_evaluar.day}",
                "value": cant_prestamos
            })
            
            # Armamos las barras (Ocupación vs Reservas)
            bar_chart_data.append({
                "name": nombre_dia,
                "series": [
                    {"name": "Préstamos", "value": cant_prestamos},
                    {"name": "Reservas", "value": cant_reservas}
                ]
            })

        line_chart_data = [{
            "name": "Préstamos",
            "series": line_series
        }]

        # --- 3. Retornar JSON ---
        return Response({
            "kpis": {
                "total_prestamos": total_prestamos,
                "nuevos_usuarios": nuevos_usuarios,
                "tasa_ocupacion": tasa_ocupacion,
                "reservas_activas": reservas_activas
            },
            "graficas": {
                "pie_chart": pie_chart_data,
                "bar_chart": bar_chart_data,
                "line_chart": line_chart_data
            }
        })
