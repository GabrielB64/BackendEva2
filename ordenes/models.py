from django.conf import settings
from django.db import models

from catalogo.models import Producto


class Orden(models.Model):
    """
    Representa una compra histórica realizada por un cliente.

    Los precios de los productos quedan congelados mediante
    los registros de DetalleOrden.
    """

    class Estado(models.TextChoices):
        PENDIENTE = "PENDIENTE", "Pendiente"
        PAGADO = "PAGADO", "Pagado"
        ENTREGADO = "ENTREGADO", "Entregado"
        CANCELADO = "CANCELADO", "Cancelado"

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="ordenes",
    )

    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.PENDIENTE,
    )

    total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    creado_en = models.DateTimeField(
        auto_now_add=True,
    )

    actualizado_en = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return f"Orden #{self.id} - {self.usuario.username}"


class DetalleOrden(models.Model):
    """
    Representa un producto específico dentro de una orden.

    Guarda una copia histórica del nombre, SKU y precio para que
    los cambios posteriores del catálogo no modifiquen la venta.
    """

    orden = models.ForeignKey(
        Orden,
        on_delete=models.CASCADE,
        related_name="detalles",
    )

    producto = models.ForeignKey(
        Producto,
        on_delete=models.PROTECT,
        related_name="detalles_orden",
    )

    nombre_producto = models.CharField(
        max_length=150,
    )

    sku = models.CharField(
        max_length=50,
    )

    precio_unitario = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    cantidad = models.PositiveIntegerField()

    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    def __str__(self):
        return f"{self.nombre_producto} x {self.cantidad}"