from rest_framework import serializers
from .models import Carro, ItemCarro

class ItemCarroSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo ItemCarro.
    """
    
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)
    producto_marca = serializers.CharField(source='producto.marca', read_only=True)
    precio_unitario = serializers.DecimalField(source='producto.precio', max_digits=12, decimal_places=0, read_only=True)
    subtotal = serializers.SerializerMethodField()
    
    class Meta:
        model = ItemCarro
        fields = (
            'id', 
            'producto',
            'producto_nombre',
            'producto_marca',
            'precio_unitario',
            'cantidad',
            'subtotal',
        )
    
    def get_subtotal(self, obj):
        return obj.cantidad * obj.producto.precio
    

class CarroSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Carro.
    """
    
    items = ItemCarroSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()
    
    class Meta:
        model = Carro
        fields = (
            'id', 
            'items',
            'total',
        )
        
    def get_total(self, obj):
        return sum(
            item.producto.precio * item.cantidad for item in obj.items.all()
        )