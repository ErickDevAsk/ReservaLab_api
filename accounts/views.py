from django.shortcuts import render
from rest_framework import generics, viewsets # 👈 Agregamos viewsets
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model


# 👇 Importamos los dos serializers que ya tienes
from .serializers import RegisterSerializer, TecnicoSerializer
# 👇 Importamos el permiso estricto del jefe
from .permissions import IsAdminRole
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, UserProfileSerializer

from .serializers import RegisterSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


User = get_user_model()

# ==========================================
# 🚪 PUERTA PÚBLICA: REGISTRO DE ESTUDIANTES
# ==========================================
class RegisterView(generics.CreateAPIView):
    # Definimos de dónde va a sacar la estructura (del modelo personalizado)
    queryset = User.objects.all()
    
    # REGLA DE ORO: Permitimos que cualquier persona entre a esta vista sin estar logueada.
    permission_classes = (AllowAny,)
    
    # Le conectamos el serializer de registro
    serializer_class = RegisterSerializer

# ==========================================
# 🛡️ PUERTA VIP: CRUD DE TÉCNICOS (SOLO ADMIN)
# ==========================================
class TecnicoViewSet(viewsets.ModelViewSet):
    serializer_class = TecnicoSerializer
    
    # ¡CANDADO PUESTO! Solo el Admin pasa de aquí
    permission_classes = [IsAdminRole]

    def get_queryset(self):
        # Para que el Admin no vea la lista de todos los estudiantes, 
        # filtramos la base de datos para que solo devuelva a los que son Técnicos.
        return User.objects.filter(rol__nombre_rol='Tecnico')
# ESTA ES LA VISTA PARA EL PERFIL
class PerfilUsuarioView(generics.RetrieveUpdateAPIView):
    """
    Vista que permite al estudiante ver (GET) y actualizar (PATCH) 
    su propia información de perfil.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # En lugar de buscar un ID en la URL, retornamos 
        # directamente al usuario que está autenticado.
        return self.request.user

class CustomTokenSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # 🔥 ESTE ES EL FIX REAL
        token['rol'] = user.rol.nombre_rol.lower()

        return token


class CustomTokenView(TokenObtainPairView):
    serializer_class = CustomTokenSerializer

