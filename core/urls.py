from django.contrib import admin
from django.urls import path
from django.http import JsonResponse
from rest_framework_simplejwt.views import TokenObtainPairView # <--- ESTO ES LO QUE FALTA

def api_root(request):
    return JsonResponse({"mensaje": "Backend Operando"})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', api_root),
    # Esta línea es la que quita el error 404:
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]