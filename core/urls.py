from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from accounts.views import CustomTokenView 

def api_root(request):
    return JsonResponse({"mensaje": "Backend Operando"})



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', api_root),


    #  2. USAMOS VISTA PARA EL TOKEN
    path('api/token/', CustomTokenView.as_view(), name='token_obtain_pair'),
    
    path('api/', include('equipment.urls')),
    path('api/labs/', include('labs.urls')),
    path('api/reservas/', include('reservations.urls')),
    
    path('api/accounts/', include('accounts.urls')), 
    
    path('api/loans/', include('loans.urls')),

    path('api/dashboard/', include('dashboard.urls')),
]