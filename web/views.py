from django.shortcuts import render


def home(request):
    """
    Página principal de la tienda.
    """

    return render(
        request,
        "home.html",
    )