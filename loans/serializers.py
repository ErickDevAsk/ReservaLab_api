from rest_framework import serializers
from .models import Prestamo  # 👈 usa tu modelo real

class LoanSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.CharField(source='usuario.username', read_only=True)
    equipo_nombre = serializers.CharField(source='equipo.nombre', read_only=True)

    class Meta:
        model = Prestamo
        fields = '__all__'