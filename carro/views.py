from django.shortcuts import get_object_or_404, render, redirect
from django.db import transaction
from django.contrib.auth.decorators import login_required

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from catalogo.models import Producto

from .models import Carro, ItemCarro
from .serializers import CarroSerializer, ItemCarroSerializer


class CarroDetailView(generics.RetrieveAPIView):
    """
    Permite al cliente autenticado consultar su carrito persistente.
    """

    serializer_class = CarroSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        carro, created = Carro.objects.get_or_create(
            usuario=self.request.user
        )

        return carro


class CarroAgregarView(generics.CreateAPIView):
    """
    Agrega un producto al carrito del usuario autenticado.

    Si el producto ya existe dentro del carrito, se incrementa
    su cantidad.
    """

    serializer_class = ItemCarroSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        producto_id = request.data.get("producto")
        cantidad = request.data.get("cantidad", 1)

        try:
            cantidad = int(cantidad)
        except (TypeError, ValueError):
            return Response(
                {"error": "La cantidad debe ser un número entero."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if cantidad <= 0:
            return Response(
                {"error": "La cantidad debe ser mayor que cero."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        producto = get_object_or_404(
            Producto,
            id=producto_id,
            activo=True,
        )

        carro, created = Carro.objects.get_or_create(
            usuario=request.user
        )

        item, creado = ItemCarro.objects.get_or_create(
            carro=carro,
            producto=producto,
            defaults={
                "cantidad": cantidad,
            },
        )

        if not creado:
            item.cantidad += cantidad
            item.save()

        serializer = self.get_serializer(item)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )


class CarroEliminarView(generics.DestroyAPIView):
    """
    Elimina un producto del carrito del usuario autenticado.
    """

    serializer_class = ItemCarroSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        carro, created = Carro.objects.get_or_create(
            usuario=self.request.user
        )

        return ItemCarro.objects.filter(
            carro=carro
        )
        
def carro_html(request):
    """
    Página HTML del carrito persistente del usuario autenticado.
    """

    carro, created = Carro.objects.get_or_create(
        usuario=request.user
    )

    return render(
        request,
        "carro/carrito.html",
        {
            "carro": carro,
        },
    )
    
def carro_eliminar_html(request, pk):
    """
    Elimina un producto del carrito desde la interfaz HTML.
    """

    if request.method == "POST":
        carro = get_object_or_404(
            Carro,
            usuario=request.user,
        )

        item = get_object_or_404(
            ItemCarro,
            id=pk,
            carro=carro,
        )

        item.delete()

    return redirect("carro-html")

@login_required
def carro_agregar_html(request):
    if request.method == "POST":
        producto_id = request.POST.get("producto")
        cantidad = int(request.POST.get("cantidad", 1))

        if cantidad < 1:
            cantidad = 1

        producto = get_object_or_404(
            Producto,
            id=producto_id,
            activo=True,
        )

        carro, _ = Carro.objects.get_or_create(
            usuario=request.user
        )

        item, creado = ItemCarro.objects.get_or_create(
            carro=carro,
            producto=producto,
            defaults={"cantidad": cantidad},
        )

        if not creado:
            item.cantidad += cantidad
            item.save()

    return redirect("carro-html")