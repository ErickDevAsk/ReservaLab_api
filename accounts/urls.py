from django.urls import path
from .views import RegisterView, PerfilUsuarioView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    # 👇 RUTA PARA CONSULTAR Y EDITAR EL PERFIL 👇
    path('perfil/', PerfilUsuarioView.as_view(), name='perfil'),
]