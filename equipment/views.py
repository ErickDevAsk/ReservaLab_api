from rest_framework import viewsets
from .models import Equipo
from .serializers import EquipoSerializer
# nuestro cadenero desde accounts
from accounts.permissions import IsAdminOrTecnico 

class EquipoViewSet(viewsets.ModelViewSet):
    queryset = Equipo.objects.all()
    serializer_class = EquipoSerializer
    
    # CANDADO
    permission_classes = [IsAdminOrTecnico]