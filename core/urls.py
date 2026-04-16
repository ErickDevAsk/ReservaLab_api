from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

from rest_framework_simplejwt.views import TokenObtainPairView # <--- ESTO ES LO QUE FALTA
from django.urls import path, include

from rest_framework_simplejwt.views import TokenObtainPairView
from accounts.serializers import CustomTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

def api_root(request):
    return JsonResponse({"mensaje": "Backend Operando"})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', api_root),

    # Esta línea es la que quita el error 404:
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/', include('equipment.urls')),

    path('labs/', include('labs.urls')),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/reservas/', include('reservations.urls')),
    # Comentamos esta línea temporalmente para que no truene si no tienes el archivo
    path('api/accounts/', include('accounts.urls')), 

]