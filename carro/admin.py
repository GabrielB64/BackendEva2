from django.contrib import admin
from .models import Carro, ItemCarro
# Register your models here.

@admin.register(Carro)
class CarroAdmin(admin.ModelAdmin):
    """
    Configuración de los carritos dentr del administrador.
    """
    
    list_display = ('usuario', 'creado_en', 'actualizado_en')
    search_fields = ('usuario__username', 'usuario__email')
    
@admin.register(ItemCarro)
class ItemCarroAdmin(admin.ModelAdmin):
    """
    Configuración de los ítems de los carritos dentro del administrador.
    """
    
    list_display = ('carro', 'producto', 'cantidad', 'agregado_en',)
    search_fields = ('carro__usuario__username', 'producto__nombre', 'producto__sku',)
    