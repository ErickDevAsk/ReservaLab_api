from django.urls import path
from .views import AprobarReservaView, CrearReservaView, RechazarReservaView

urlpatterns = [
    path('crear/', CrearReservaView.as_view(), name='crear_reserva'),
    # 👇 Nuestras nuevas rutas dinámicas que reciben el ID (<int:pk>) de la reserva
    path('<int:pk>/aprobar/', AprobarReservaView.as_view(), name='aprobar_reserva'),
    path('<int:pk>/rechazar/', RechazarReservaView.as_view(), name='rechazar_reserva'),
]