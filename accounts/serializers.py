from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from .models import Rol

User = get_user_model() 

# --->  EL SERIALIZER PARA EL LOGIN <---
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['rol'] = str(user.rol) if user.rol else None
        token['username'] = user.username
        return token

# ---> EL SERIALIZER PARA EL REGISTRO <---
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        #Usamos los nombres reales del modelo
        fields = ['username', 'email', 'password', 'matricula_id', 'carrera_departamento']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            matricula_id=validated_data.get('matricula_id', ''),
            carrera_departamento=validated_data.get('carrera_departamento', '')
        )

        try:
            rol_estudiante = Rol.objects.get(nombre_rol='Estudiante') 
            user.rol = rol_estudiante
            user.save()
        except Rol.DoesNotExist:
            print("🚨 ALERTA: No existe el rol 'Estudiante' en la base de datos.")
            user.save()
            
        return user
    
# ---> EL SERIALIZER PARA EL PERFIL (GET y PATCH) <---
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User # Usamos la variable User que ya tienes definida arriba
        fields = [
            'username', 'email', 'matricula_id', 'carrera_departamento', 
            'telefono', 'equipo_registrado', 'habilidades'
        ]
        # Bloqueamos estos campos para que nadie pueda cambiarlos desde el perfil de Angular
        read_only_fields = ['username', 'email', 'matricula_id', 'carrera_departamento']
