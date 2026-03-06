from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # El truco está aquí: convertimos el objeto Rol a simple texto
        # (y le ponemos el if por si hay un usuario que no tenga rol asignado)
        token['rol'] = str(user.rol) if user.rol else None
        token['username'] = user.username
        
        return token