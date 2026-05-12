from django.urls import path
from .views import AdminDashboardView, TecnicoDashboardView, TecnicoReportesView

urlpatterns = [
    path('admin/', AdminDashboardView.as_view(), name='dashboard-admin'),
    path('tecnico/', TecnicoDashboardView.as_view(), name='dashboard-tecnico'),
    path('tecnico/reportes/', TecnicoReportesView.as_view(), name='reportes-tecnico'),
]