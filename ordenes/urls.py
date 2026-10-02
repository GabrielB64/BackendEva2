from django.urls import path

from .views import (
    CheckoutView,
    MisOrdenesView,
    OrdenEstadoView,
    mis_ordenes_html,
)


urlpatterns = [
    path(
        "checkout/",
        CheckoutView.as_view(),
        name="checkout",
    ),

    path(
        "mis-ordenes/",
        MisOrdenesView.as_view(),
        name="mis-ordenes",
    ),

    path(
        "<int:pk>/estado/",
        OrdenEstadoView.as_view(),
        name="orden-estado",
    ),
    
    path(
        "mis-ordenes/",
        mis_ordenes_html,
        name="mis-ordenes-html",
    ),
]