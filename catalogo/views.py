from django.shortcuts import get_object_or_404, render

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from .models import Producto, Categoria
from .serializers import ProductoSerializer, CategoriaSerializer

from usuarios.permissions import EsAdministrador
from rest_framework.permissions import AllowAny, IsAuthenticated

# Create your views here.

class CategoriaListView(generics.ListCreateAPIView):
    """
    Vista para listar y crear categorías de productos.
    Solo los usuarios con rol de 'Administrador' pueden crear nuevas categorías.
    """
    
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    
    def get_permissions(self):
        """
        Asigna permisos según el método HTTP.
        GET: Permite a cualquier usuario autenticado listar categorías.
        POST: Restringe la creación de categorías a administradores.
        """
        if self.request.method == 'POST':
            return [EsAdministrador()]
        return [AllowAny()]  # Permite a cualquier usuario autenticado listar categorías
    
class CategoriaDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Permite consultar, modificar y eliminar una categoría.
    La consulta es pública.
    Las modificaciones requieren que el usuario sea un administrador.
    """
    
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    
    def get_permissions(self):
        """
        La consulta individual es pública.
        
        PUT, PATCH y DELETE requieren que el usuario sea un administrador.
        """
        
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [EsAdministrador()]
        return [AllowAny()]
    
class ProductoListView(generics.ListCreateAPIView):
    """
    Vista para listar y crear productos.
    Solo los usuarios con rol de 'Administrador' pueden crear nuevos productos.
    """
    
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'categoria',
        'marca',
        'activo',
    ]
    
    def get_permissions(self):
        """
        Asigna permisos según el método HTTP.
        GET: Permite a cualquier usuario autenticado listar productos.
        POST: Restringe la creación de productos a administradores.
        """
        if self.request.method == 'POST':
            return [EsAdministrador()]
        return [AllowAny()]  # Permite a cualquier usuario autenticado listar 
    
class ProductoDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Permite consultar, modificar y eliminar un producto.
    
    La consulta es pública.
    Las modificaciones requieren que el usuario sea un administrador.
    """
    
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    
    def get_permissions(self):
        """
        La consulta individual es pública.
        
        PUT, PATCH y DELETE requieren que el usuario sea un administrador.
        """
        
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [EsAdministrador()]
        return [AllowAny()]
    
def catalogo_html(request):
    """
    Página HTML pública del catálogo de productos.
    """

    productos = Producto.objects.filter(
        activo=True
    ).select_related(
        "categoria"
    )

    return render(
        request,
        "catalogo/lista.html",
        {
            "productos": productos,
        },
    )

def producto_html(request, pk):
    """
    Página HTML con el detalle de un producto.
    """

    producto = get_object_or_404(
        Producto.objects.select_related("categoria"),
        pk=pk,
        activo=True,
    )

    return render(
        request,
        "catalogo/detalle.html",
        {
            "producto": producto,
        },
    )