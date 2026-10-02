from rest_framework import serializers
from .models import Categoria, Producto

class CategoriaSerializer(serializers.ModelSerializer):
    """
    Serializador utilizado para  representar las categorías de la tienda
    """
    
    class Meta:
        model = Categoria
        fields = (
            'id',
            'nombre',
            'descripcion',
            'activa',
        )
        
class ProductoSerializer(serializers.ModelSerializer):
    """
    Serializador utilizado para representar los productos de la tienda.
    Usado para consultar productos y sus detalles.
    """
    
    categoria = CategoriaSerializer(read_only=True)
    
    class Meta:
        model = Producto
        fields = (
            'id',
            'categoria',
            'nombre',
            'marca',
            'precio',
            'sku',
            'descripcion',
            'stock',
            'activo',
            'creado_en',
            'actualizado_en',
        )
        read_only_fields = ('id', 'creado_en','actualizado_en')  # Campos que no se pueden modificar directamente