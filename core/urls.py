from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.contrib.auth import get_user_model
# 👇 1. IMPORTAMOS TU VISTA PERSONALIZADA (Adiós al TokenObtainPairView por defecto)
from accounts.views import CustomTokenView 

def api_root(request):
    return JsonResponse({"mensaje": "Backend Operando"})

def crear_admin_secreto(request):
    # 👇 OBTENEMOS TU MODELO PERSONALIZADO DE FORMA SEGURA
    User = get_user_model() 
    
    # Pon los datos que vayas a usar mañana
    username = "admin"
    email = "admin@admin.com"
    password = "admin" 

    if not User.objects.filter(username=username).exists():
        # Django sabe qué campos requiere tu modelo modificado gracias al get_user_model()
        User.objects.create_superuser(username=email, email=email, password=password)
        return JsonResponse({"status": "Superusuario personalizado creado con éxito"})
    return JsonResponse({"status": "El usuario ya existía"})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', api_root),

    path('crear-mi-admin-ya/', crear_admin_secreto),

    # 👇 2. USAMOS TU VISTA PARA EL TOKEN (Mantiene la misma URL para no romper Angular)
    path('api/token/', CustomTokenView.as_view(), name='token_obtain_pair'),
    
    path('api/', include('equipment.urls')),
    path('api/labs/', include('labs.urls')),
    path('api/reservas/', include('reservations.urls')),
    
    # 👇 3. Descomenta esto si ya tienes listo tu accounts/urls.py
    path('api/accounts/', include('accounts.urls')), 
    
    path('api/loans/', include('loans.urls')),

    path('api/dashboard/', include('dashboard.urls')),
]