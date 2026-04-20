from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, UserProfileSerializer

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    # Definimos de dónde va a sacar la estructura (del modelo personalizado)
    queryset = User.objects.all()
    
    # REGLA DE ORO: Permitimos que cualquier persona entre a esta vista sin estar logueada.
    # Si no ponemos AllowAny, Django pediría un token para poder registrarse (lo cual es imposible porque apenas se van a registrar).
    permission_classes = (AllowAny,)
    
    # Le conectamos el serializer que acabas de hacer
    serializer_class = RegisterSerializer

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