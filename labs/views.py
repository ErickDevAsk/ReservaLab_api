from rest_framework import viewsets
from .models import Laboratorio
from .serializers import LaboratorioSerializer

class LaboratorioViewSet(viewsets.ModelViewSet):
    queryset = Laboratorio.objects.all()
    serializer_class = LaboratorioSerializer