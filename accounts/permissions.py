from rest_framework import permissions

class IsAdminOrTecnico(permissions.BasePermission):
    """
    Permiso para que solo Admins y Técnicos puedan gestionar equipos y labs.
    """
    def has_permission(self, request, view):
        # 1. Verificamos que esté logueado
        if not bool(request.user and request.user.is_authenticated):
            return False
            
        # 2. Verificamos que tenga un rol asignado
        if not request.user.rol:
            return False
            
        # 3. Solo pasan si su rol es 'Admin' o 'Tecnico'
        return request.user.rol.nombre_rol in ['Administrador', 'Tecnico']


class IsAdminRole(permissions.BasePermission):
    """
    Permiso VIP: SOLO el Admin puede entrar aquí (para el CRUD de Técnicos).
    """
    def has_permission(self, request, view):
        if not bool(request.user and request.user.is_authenticated):
            return False
            
        if not request.user.rol:
            return False
            
        # Solo pasa el jefe
        return request.user.rol.nombre_rol == 'Administrador'