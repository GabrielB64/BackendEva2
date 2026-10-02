from django.db import models
from django.conf import settings

from catalogo.models import Producto

# Create your models here.

class Carro(models.Model):
    """
    Representa un carrito de compras asociado a un usuario.
    Un usuario puede tener un solo carrito activo a la vez.
    """
    
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='carro',
        help_text="Usuario al que pertenece el carrito."
    )
    
    creado_en = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha y hora en que se creó el carrito."
    )
    
    actualizado_en = models.DateTimeField(
        auto_now=True,
        help_text="Fecha y hora de la última actualización del carrito."
    )
    
    def __str__(self):
        return f"Carro de {self.usuario.username}"
    
class ItemCarro(models.Model):
    """
    Representa un ítem dentro de un carrito de compras.
    Cada ítem está asociado a un producto y a un carrito específico.
    """
    
    carro = models.ForeignKey(
        Carro, 
        on_delete=models.CASCADE, 
        related_name='items',
        help_text="Carrito al que pertenece este ítem."
    )
    
    producto = models.ForeignKey(
        Producto, 
        on_delete=models.CASCADE,
        related_name='items_carro',
        help_text="Producto asociado a este ítem del carrito."
    )
    
    cantidad = models.PositiveIntegerField(
        default=1,
        help_text="Cantidad del producto en el carrito."
    )
    
    agregado_en = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha y hora en que se agregó el ítem al carrito."
    )
    
    class Meta: 
        constraints = [
            models.UniqueConstraint(
                fields=['carro', 'producto'], 
                name='un_producto_por_carro',
            ),
        ]
        
    def __str__(self):
        return (
            f"{self.producto.nombre} "
            f"x {self.cantidad}"
        )
    