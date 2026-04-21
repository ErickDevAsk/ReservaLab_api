from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    # Definimos de dónde va a sacar la estructura (del modelo personalizado)
    queryset = User.objects.all()
    
    # REGLA DE ORO: Permitimos que cualquier persona entre a esta vista sin estar logueada.
    # Si no ponemos AllowAny, Django pediría un token para poder registrarse (lo cual es imposible porque apenas se van a registrar).
    permission_classes = (AllowAny,)
    
    # Le conectamos el serializer que acabas de hacer
    serializer_class = RegisterSerializer

class CustomTokenSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # 🔥 ESTE ES EL FIX REAL
        token['rol'] = user.rol.nombre_rol.lower()

        return token


class CustomTokenView(TokenObtainPairView):
    serializer_class = CustomTokenSerializer