from rest_framework.permissions import BasePermission
from .models import Usuario

class EsAdministrador(BasePermission):
    """
    Permiso personalizado que permite acceder únicamente a usuarios
    autenticados con el rol de 'Administrador'.
    """
    
    message = "Acceso denegado. Se requiere ser un administrador para acceder a este recurso."
    
    def has_permission(self, request, view):
        return(
            request.user and
            request.user.is_authenticated and
            request.user.rol == Usuario.Rol.ADMINISTRADOR
        )