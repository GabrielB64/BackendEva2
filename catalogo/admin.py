from django.contrib import admin
from .models import Categoria, Producto

# Register your models here.

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    """
    Configuración de las categorías en el panel de administración de Django.
    """
    
    list_display = (
        'nombre',
        'activa',
    )
    
    search_fields = ('nombre',)
    
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    """
    Configuración de los productos en el panel de administración de Django.
    """
    
    list_display = (
        'nombre',
        'marca',
        'categoria',
        'precio',
        'stock',
        'activo',
    )
    
    search_fields = ('nombre', 'marca', 'sku',)
    
    list_filter = ('categoria', 'marca','activo',)