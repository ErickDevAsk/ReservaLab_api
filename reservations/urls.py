from django.urls import path
from .views import AprobarReservaView, CrearReservaView, MisReservasView, RechazarReservaView,ListarReservasPorLaboratorioView

urlpatterns = [
    path('crear/', CrearReservaView.as_view(), name='crear_reserva'),
    # 👇 Nuestras nuevas rutas dinámicas que reciben el ID (<int:pk>) de la reserva
    path('<int:pk>/aprobar/', AprobarReservaView.as_view(), name='aprobar_reserva'),
    path('<int:pk>/rechazar/', RechazarReservaView.as_view(), name='rechazar_reserva'),
    path('laboratorio/<int:laboratorio_id>/', ListarReservasPorLaboratorioView.as_view(), name='listar_reservas_lab'),
    path('mis-reservas/', MisReservasView.as_view(), name='mis-reservas'),
]