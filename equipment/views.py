from rest_framework import viewsets
from .models import Equipo
from .serializers import EquipoSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
# nuestro cadenero desde accounts
from accounts.permissions import IsAdminOrTecnico 

class EquipoViewSet(viewsets.ModelViewSet):
    queryset = Equipo.objects.all()
    serializer_class = EquipoSerializer
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated]
        return [IsAdminOrTecnico()]