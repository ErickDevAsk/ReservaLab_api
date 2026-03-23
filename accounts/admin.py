from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Rol

# Creamos nuestro propio panel de administrador basado en el original
class CustomUserAdmin(UserAdmin):
    # 1. Le decimos a Django que agregue una sección nueva en la pantalla de edición
    fieldsets = UserAdmin.fieldsets + (
        ('Información de ReservaLab', {'fields': ('rol', 'matricula_id', 'carrera_departamento')}),
    )
    
    # 2. (Opcional pero pro) Mostramos el rol como una columna extra en la tabla principal
    list_display = ('username', 'email', 'first_name', 'last_name', 'rol')

admin.site.register(Rol)
# 3. Registramos al usuario usando nuestra nueva clase en lugar de la original
admin.site.register(Usuario, CustomUserAdmin)