from django.urls import path, include
from rest_framework.routers import DefaultRouter

# 👇 Traemos tus dos vistas
from .views import RegisterView, TecnicoViewSet

# 1. Creamos el enrutador mágico de DRF
router = DefaultRouter()

# 2. Le conectamos el CRUD de Técnicos
# Esto crea en automático: 
# GET /tecnicos/ (lista), POST /tecnicos/ (crear), PUT /tecnicos/5/ (editar), DELETE /tecnicos/5/ (borrar)
router.register(r'tecnicos', TecnicoViewSet, basename='tecnicos')

from django.urls import path

from .views import RegisterView, PerfilUsuarioView

from .views import RegisterView, CustomTokenView


urlpatterns = [
    # Tu ruta pública original se queda intacta
    path('register/', RegisterView.as_view(), name='register'),

    
    # 3. Enchufamos todas las rutas del router a nuestra app
    path('', include(router.urls)),
    # 👇 RUTA PARA CONSULTAR Y EDITAR EL PERFIL 👇
    path('perfil/', PerfilUsuarioView.as_view(), name='perfil'),

    path('token/', CustomTokenView.as_view(), name='token'),

]