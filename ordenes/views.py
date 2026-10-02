from django.db import transaction

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from carro.models import Carro
from .models import DetalleOrden, Orden
from .serializers import OrdenSerializer

from django.shortcuts import get_object_or_404, render, redirect
from usuarios.permissions import EsAdministrador


class CheckoutView(APIView):
    """
    Convierte el carrito activo del usuario en una orden.

    El stock se valida y descuenta dentro de una transacción
    atómica para evitar inconsistencias en el inventario.
    """

    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        carro, created = Carro.objects.get_or_create(
            usuario=request.user
        )

        items = carro.items.select_related(
            "producto"
        ).select_for_update()

        if not items.exists():
            return Response(
                {
                    "error": "El carrito está vacío."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        total = 0
        detalles = []

        for item in items:
            producto = item.producto

            if not producto.activo:
                return Response(
                    {
                        "error": (
                            f"El producto "
                            f"{producto.nombre} "
                            f"ya no está disponible."
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if producto.stock < item.cantidad:
                return Response(
                    {
                        "error": (
                            f"Stock insuficiente para "
                            f"{producto.nombre}."
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            subtotal = producto.precio * item.cantidad
            total += subtotal

            detalles.append(
                {
                    "producto": producto,
                    "nombre_producto": producto.nombre,
                    "sku": producto.sku,
                    "precio_unitario": producto.precio,
                    "cantidad": item.cantidad,
                    "subtotal": subtotal,
                }
            )

        orden = Orden.objects.create(
            usuario=request.user,
            estado=Orden.Estado.PAGADO,
            total=total,
        )

        for detalle in detalles:
            producto = detalle["producto"]

            producto.stock -= detalle["cantidad"]
            producto.save(
                update_fields=["stock"]
            )

            DetalleOrden.objects.create(
                orden=orden,
                producto=producto,
                nombre_producto=detalle["nombre_producto"],
                sku=detalle["sku"],
                precio_unitario=detalle["precio_unitario"],
                cantidad=detalle["cantidad"],
                subtotal=detalle["subtotal"],
            )

        items.delete()

        return Response(
            OrdenSerializer(orden).data,
            status=status.HTTP_201_CREATED,
        )
        
class MisOrdenesView(APIView):
    """
    Devuelve únicamente las órdenes pertenecientes al usuario
    autenticado.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        ordenes = Orden.objects.filter(
            usuario=request.user
        ).prefetch_related(
            "detalles"
        )

        serializer = OrdenSerializer(
            ordenes,
            many=True,
        )

        return Response(serializer.data)
    
class OrdenEstadoView(APIView):
    """
    Permite al administrador cambiar el estado de una orden.

    Las órdenes pagadas pueden ser entregadas o canceladas.
    Al cancelar una orden pagada, se repone el stock.
    """

    permission_classes = [EsAdministrador]

    @transaction.atomic
    def patch(self, request, pk):
        orden = get_object_or_404(
            Orden.objects.select_for_update(),
            pk=pk,
        )

        nuevo_estado = request.data.get("estado")

        estados_validos = [
            Orden.Estado.ENTREGADO,
            Orden.Estado.CANCELADO,
        ]

        if nuevo_estado not in estados_validos:
            return Response(
                {
                    "error": (
                        "El estado debe ser ENTREGADO "
                        "o CANCELADO."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if orden.estado != Orden.Estado.PAGADO:
            return Response(
                {
                    "error": (
                        "Solo se pueden modificar "
                        "órdenes PAGADO."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if nuevo_estado == Orden.Estado.CANCELADO:
            for detalle in orden.detalles.select_related(
                "producto"
            ).select_for_update():

                producto = detalle.producto
                producto.stock += detalle.cantidad

                producto.save(
                    update_fields=["stock"]
                )

        orden.estado = nuevo_estado
        orden.save(
            update_fields=[
                "estado",
                "actualizado_en",
            ]
        )

        return Response(
            OrdenSerializer(orden).data
        )

def mis_ordenes_html(request):
    """
    Página HTML que muestra el historial de órdenes del usuario autenticado.
    """

    ordenes = Orden.objects.filter(
        usuario=request.user
    ).prefetch_related(
        "detalles"
    )

    return render(
        request,
        "ordenes/mis_ordenes.html",
        {
            "ordenes": ordenes,
        },
    )