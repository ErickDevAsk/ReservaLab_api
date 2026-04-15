"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from rest_framework_simplejwt.views import TokenObtainPairView
from accounts.serializers import CustomTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

def api_root(request):
    return JsonResponse({
        "proyecto": "ReservaLab BUAP",
        "estado": "Backend Operando",
        "versiones": {
            "python": "3.13",
            "django": "6.0.2"
        },
        "mensaje": "¡Hola Profe! Infraestructura lista."
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', api_root),
    path('labs/', include('labs.urls')),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/reservas/', include('reservations.urls')),
    # Comentamos esta línea temporalmente para que no truene si no tienes el archivo
    path('api/accounts/', include('accounts.urls')), 
]