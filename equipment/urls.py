from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import EquipoViewSet, IncidenciaAPIView

router = DefaultRouter()
router.register(r'equipos', EquipoViewSet)

urlpatterns = [
    path('equipos/incidencias/', IncidenciaAPIView.as_view(), name='gestion-incidencias'),

    
]

urlpatterns += router.urls

