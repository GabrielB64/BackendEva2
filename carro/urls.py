from django.urls import path

from .views import (
    CarroAgregarView,
    CarroDetailView,
    CarroEliminarView,
    carro_agregar_html,
    carro_eliminar_html,
    carro_html,
)


urlpatterns = [
    path(
        "",
        CarroDetailView.as_view(),
        name="carro",
    ),

    path(
        "agregar/",
        CarroAgregarView.as_view(),
        name="carro-agregar",
    ),

    path(
        "eliminar/<int:pk>/",
        CarroEliminarView.as_view(),
        name="carro-eliminar",
    ),

    path(
        "html/",
        carro_html,
        name="carro-html",
    ),
    
    path(
        "pagina/eliminar/<int:pk>/",
        carro_eliminar_html,
        name="carro-eliminar-html",
    ),
    path(
    "pagina/agregar/",
    carro_agregar_html,
    name="carro-agregar-html",
),
    
]