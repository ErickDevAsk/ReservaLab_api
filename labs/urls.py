from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LaboratorioViewSet

router = DefaultRouter()
router.register(r'laboratorios', LaboratorioViewSet)

urlpatterns = [
    path('', include(router.urls)),
]