from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class Usuario(AbstractUser):
    """
    Modelo de usuario personalizado para la tienda.
    
    Hereda de AbstractUser para conservar la funcionalidad de autenticación de Django.
    
    Se agrega el campo rol para diferenciar entre usuarios normales y administradores.
    """

    class Rol(models.TextChoices):
        CLIENTE = 'CLIENTE', 'Cliente'
        ADMINISTRADOR = 'ADMINISTRADOR', 'Administrador'
        
    rol = models.CharField(
        max_length=20,
        choices=Rol.choices,
        default=Rol.CLIENTE,
        help_text="Rol del usuario en la tienda. Puede ser 'Cliente' o 'Administrador'."
    )
    
    def __str__(self):
        return self.username