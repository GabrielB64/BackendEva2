from django.db import models

# Create your models here.

class Categoria(models.Model):
    """ 
    Representa una categoría de productos en la tienda.
    
    Una categoría puede tener múltiples productos asociados a ella.
    """
    
    nombre = models.CharField(
        max_length=100, 
        unique=True, 
        help_text="Nombre único de la categoría."
    )
    
    descripcion = models.TextField(
        blank=True, 
        help_text="Descripción opcional de la categoría."
    )
    
    activa = models.BooleanField(
        default=True, 
        help_text="Indica si la categoría está activa y visible en la tienda."
    )
    
    def __str__(self):
        return self.nombre
    
class Producto(models.Model):
    """
    Representa un producto en la tienda.
    
    Cada producto pertenece a una categoría y tiene atributos como precio, stock y disponibilidad.
    """
    
    categoria = models.ForeignKey(
        Categoria, 
        on_delete=models.CASCADE, 
        related_name='productos',
        help_text="Categoría a la que pertenece el producto."
    )
    
    nombre = models.CharField(
        max_length=200,
        help_text="Nombre del producto."
    )
    
    marca = models.CharField(
        max_length=100,
        help_text="Marca del producto."
    )
    
    precio = models.DecimalField(
        max_digits=12, 
        decimal_places=0,
        help_text="Precio del producto en la moneda local."
    )
    
    sku = models.CharField(
        max_length=50, 
        unique=True,
        help_text="Código único de identificación del producto (SKU)."
    )
    
    descripcion = models.TextField(
        blank=True,
        help_text="Descripción detallada del producto."
    )
    
    stock = models.PositiveIntegerField(
        default=0,
        help_text="Cantidad disponible en inventario."
    )
    
    activo = models.BooleanField(
        default=True,
        help_text="Indica si el producto está activo y disponible para la venta."
    )
    
    creado_en = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha y hora en que el producto fue creado."
    )
    
    actualizado_en = models.DateTimeField(
        auto_now=True,
        help_text="Fecha y hora de la última actualización del producto."
    )
    
    def __str__(self):
        return f"{self.nombre} ({self.marca})"