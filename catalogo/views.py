from django.shortcuts import get_object_or_404, redirect, render

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from usuarios.models import Usuario
from .models import Producto, Categoria
from .serializers import ProductoSerializer, CategoriaSerializer
from django.db.models import Q

from usuarios.permissions import EsAdministrador
from rest_framework.permissions import AllowAny, IsAuthenticated

from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

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
    productos = Producto.objects.filter(
        activo=True
    ).select_related("categoria")

    # Búsqueda por nombre, marca o SKU.
    busqueda = request.GET.get("q", "").strip()

    if busqueda:
        productos = productos.filter(
            Q(nombre__icontains=busqueda)
            | Q(marca__icontains=busqueda)
            | Q(sku__icontains=busqueda)
        )

    # Filtro por categoría.
    categoria = request.GET.get("categoria", "").strip()

    if categoria:
        productos = productos.filter(categoria_id=categoria)

    # Filtro por precio mínimo.
    precio_min = request.GET.get("precio_min", "").strip()

    if precio_min:
        productos = productos.filter(precio__gte=precio_min)

    # Filtro por precio máximo.
    precio_max = request.GET.get("precio_max", "").strip()

    if precio_max:
        productos = productos.filter(precio__lte=precio_max)

    categorias = Categoria.objects.filter(activa=True).order_by("nombre")

    return render(
        request,
        "catalogo/lista.html",
        {
            "productos": productos,
            "categorias": categorias,
            "busqueda": busqueda,
            "categoria_seleccionada": categoria,
            "precio_min": precio_min,
            "precio_max": precio_max,
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
    
@login_required
def admin_productos_html(request):
    if request.user.rol != Usuario.Rol.ADMINISTRADOR:
        return redirect("home")

    productos = Producto.objects.select_related("categoria").order_by("id")

    return render(
        request,
        "catalogo/admin_productos.html",
        {"productos": productos},
    )


@login_required
def admin_producto_crear_html(request):
    if request.user.rol != Usuario.Rol.ADMINISTRADOR:
        return redirect("home")

    categorias = Categoria.objects.filter(activa=True)

    if request.method == "POST":
        Producto.objects.create(
            categoria_id=request.POST.get("categoria"),
            nombre=request.POST.get("nombre"),
            marca=request.POST.get("marca"),
            precio=request.POST.get("precio"),
            sku=request.POST.get("sku"),
            descripcion=request.POST.get("descripcion"),
            stock=request.POST.get("stock", 0),
            activo=request.POST.get("activo") == "on",
        )

        return redirect("admin-productos")

    return render(
        request,
        "catalogo/admin_producto_form.html",
        {
            "categorias": categorias,
            "titulo": "Crear producto",
        },
    )


@login_required
def admin_producto_editar_html(request, pk):
    if request.user.rol != Usuario.Rol.ADMINISTRADOR:
        return redirect("home")

    producto = get_object_or_404(Producto, pk=pk)
    categorias = Categoria.objects.filter(activa=True)

    if request.method == "POST":
        producto.categoria_id = request.POST.get("categoria")
        producto.nombre = request.POST.get("nombre")
        producto.marca = request.POST.get("marca")
        producto.precio = request.POST.get("precio")
        producto.sku = request.POST.get("sku")
        producto.descripcion = request.POST.get("descripcion")
        producto.stock = request.POST.get("stock", 0)
        producto.activo = request.POST.get("activo") == "on"

        producto.save()

        return redirect("admin-productos")

    return render(
        request,
        "catalogo/admin_producto_form.html",
        {
            "producto": producto,
            "categorias": categorias,
            "titulo": "Editar producto",
        },
    )


@login_required
@require_http_methods(["POST"])
def admin_producto_eliminar_html(request, pk):
    if request.user.rol != Usuario.Rol.ADMINISTRADOR:
        return redirect("home")

    producto = get_object_or_404(Producto, pk=pk)
    producto.delete()

    return redirect("admin-productos")