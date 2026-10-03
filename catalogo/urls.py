from django.urls import path

from .views import CategoriaListView, CategoriaDetailView, ProductoListView, ProductoDetailView, admin_producto_crear_html, admin_producto_editar_html, admin_producto_eliminar_html, admin_productos_html, catalogo_html, producto_html


urlpatterns = [
    path(
        "categorias/",
        CategoriaListView.as_view(),
        name="categorias",
    ),

    path(
        "categorias/<int:pk>/",
        CategoriaDetailView.as_view(),
        name="categoria-detalle",
    ),

    path(
        "productos/",
        ProductoListView.as_view(),
        name="productos",
    ),

    path(
        "productos/<int:pk>/",
        ProductoDetailView.as_view(),
        name="producto-detalle",
    ),
    
    path(
        "catalogo/",
        catalogo_html,
        name="catalogo",
    ),
    
    path(
        "catalogo/<int:pk>/",
        producto_html,
        name="producto-html",
    ),
    path(
    "admin-panel/productos/",
    admin_productos_html,
    name="admin-productos",
),

path(
    "admin-panel/productos/crear/",
    admin_producto_crear_html,
    name="admin-producto-crear",
),

path(
    "admin-panel/productos/<int:pk>/editar/",
    admin_producto_editar_html,
    name="admin-producto-editar",
),

path(
    "admin-panel/productos/<int:pk>/eliminar/",
    admin_producto_eliminar_html,
    name="admin-producto-eliminar",
),
]