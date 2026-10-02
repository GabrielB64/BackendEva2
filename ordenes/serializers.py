from rest_framework import serializers

from .models import DetalleOrden, Orden


class DetalleOrdenSerializer(serializers.ModelSerializer):
    """
    Serializer para representar los productos incluidos
    dentro de una orden.
    """

    class Meta:
        model = DetalleOrden
        fields = (
            "id",
            "producto",
            "nombre_producto",
            "sku",
            "precio_unitario",
            "cantidad",
            "subtotal",
        )


class OrdenSerializer(serializers.ModelSerializer):
    """
    Serializer utilizado para consultar las órdenes históricas
    de los clientes.
    """

    detalles = DetalleOrdenSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Orden
        fields = (
            "id",
            "estado",
            "total",
            "creado_en",
            "actualizado_en",
            "detalles",
        )