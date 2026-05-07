from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import EquipoViewSet, IncidenciaAPIView, ResolverIncidenciaAPIView

router = DefaultRouter()
router.register(r'equipos', EquipoViewSet)

urlpatterns = [
    path('equipos/incidencias/', IncidenciaAPIView.as_view(), name='gestion-incidencias'),
    path('equipos/incidencias/<int:pk>/resolver/', ResolverIncidenciaAPIView.as_view(), name='resolver-incidencia'),
    
]

urlpatterns += router.urls

