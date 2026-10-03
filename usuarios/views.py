from django.shortcuts import redirect, render
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer, RegistroUsuarioSerializer
from django.contrib.auth import authenticate, login, logout, get_user_model
from .models import Usuario
Usuario = get_user_model()

# Create your views here.

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Vista de autenticación que utiliza nuestro serializer JWT
    personalizado para incluir el rol del usuario en el token.
    """
    
    serializer_class = CustomTokenObtainPairSerializer
    
class RegistroUsuarioView(TokenObtainPairView):
    """
    Endpoint público para registrar nuevos usuarios. 
    Todos los usuarios registrados a través de este endpoint
    reciben automáticamente el rol de 'Cliente'.
    """
    
    serializer_class = RegistroUsuarioSerializer
    permission_classes = []
    
def login_html(request):
    """
    Página de inicio de sesión para la interfaz HTML.
    """

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        usuario = authenticate(
            request,
            username=username,
            password=password,
        )

        if usuario is not None:
            login(request, usuario)

            return redirect("home")

        return render(
            request,
            "auth/login.html",
            {
                "error": "Usuario o contraseña incorrectos.",
            },
        )

    return render(
        request,
        "auth/login.html",
    )


def logout_html(request):
    """
    Cierra la sesión HTML del usuario.
    """

    if request.method == "POST":
        logout(request)

    return redirect("home")

def registro(request):
    """
    Página de registro de nuevos clientes.
    """
    Usuario = get_user_model()

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password_confirmacion = request.POST.get(
            "password_confirmacion"
        )

        if password != password_confirmacion:

            return render(
                request,
                "auth/registro.html",
                {
                    "error": "Las contraseñas no coinciden.",
                },
            )

        if Usuario.objects.filter(
            username=username
        ).exists():

            return render(
                request,
                "auth/registro.html",
                {
                    "error": "El usuario ya existe.",
                },
            )

        usuario = Usuario.objects.create_user(
            username=username,
            email=email,
            password=password,
        )

        usuario.rol = Usuario.Rol.CLIENTE
        usuario.save()

        login(
            request,
            usuario,
        )

        return redirect("home")

    return render(
        request,
        "auth/registro.html",
    )