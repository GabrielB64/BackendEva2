from django.urls import path

from .views import CategoriaListView, CategoriaDetailView, ProductoListView, ProductoDetailView, catalogo_html, producto_html


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
]