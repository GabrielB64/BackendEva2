from django.contrib import admin

from .models import DetalleOrden, Orden


class DetalleOrdenInline(admin.TabularInline):
    model = DetalleOrden
    extra = 0
    readonly_fields = (
        "producto",
        "nombre_producto",
        "sku",
        "precio_unitario",
        "cantidad",
        "subtotal",
    )


@admin.register(Orden)
class OrdenAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "usuario",
        "estado",
        "total",
        "creado_en",
    )

    list_filter = (
        "estado",
        "creado_en",
    )

    search_fields = (
        "usuario__username",
        "usuario__email",
    )

    inlines = [
        DetalleOrdenInline,
    ]