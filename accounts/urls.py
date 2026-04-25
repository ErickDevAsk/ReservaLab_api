from django.urls import path, include
from rest_framework.routers import DefaultRouter

# 👇 Un solo import para todas tus vistas
from .views import RegisterView, TecnicoViewSet, PerfilUsuarioView, CustomTokenView

router = DefaultRouter()
router.register(r'tecnicos', TecnicoViewSet, basename='tecnicos')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('', include(router.urls)),
    path('perfil/', PerfilUsuarioView.as_view(), name='perfil'),
    
    # Aquí está tu vista personalizada
    path('token/', CustomTokenView.as_view(), name='token'),
]