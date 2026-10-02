from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario
# Register your models here.

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    """
    Configuración del modelo de usuario dentro del panel de administración de Django.
    
    Se agregan los campos propios del proyecto a la configuración estandar de UserAdmin.
    """
    
    fieldsets = UserAdmin.fieldsets + (
        (
            'Información adicional', 
            {
                'fields': ('rol',),
            },
        ),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            'Información adicional', 
            {
                'fields': ('rol',),
            },
        ),
    )