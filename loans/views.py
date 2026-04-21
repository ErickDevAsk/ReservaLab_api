from rest_framework import viewsets
from .models import Prestamo
from .serializers import LoanSerializer

class LoanViewSet(viewsets.ModelViewSet):
    queryset = Prestamo.objects.all()
    serializer_class = LoanSerializer