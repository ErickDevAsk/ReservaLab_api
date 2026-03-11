from django.urls import path
from .views import RegisterView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # Esta es la ruta que consumirá Angular: http://127.0.0.1:8000/api/accounts/register/
    path('register/', RegisterView.as_view(), name='auth_register'),
    
]