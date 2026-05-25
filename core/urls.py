from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

# 👇 1. IMPORTAMOS TU VISTA PERSONALIZADA (Adiós al TokenObtainPairView por defecto)
from accounts.views import CustomTokenView 

def api_root(request):
    return JsonResponse({"mensaje": "Backend Operando"})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', api_root),

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