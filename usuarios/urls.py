from django.urls import path
from .views import CustomTokenObtainPairView, RegistroUsuarioView
from rest_framework_simplejwt.views import TokenRefreshView

from .views import login_html, logout_html, registro

urlpatterns = [
    path(
        'login/', 
        CustomTokenObtainPairView.as_view(), 
        name='token_obtain_pair'
        ),
    path(
        'refresh/', 
        TokenRefreshView.as_view(), 
        name='token_refresh'
        ),
    path(
        'registro/',
        RegistroUsuarioView.as_view(),
        name='registro_usuario'
    ),
    path(
        'pagina/login/',
        login_html,
        name='login-html'
    ),
    path(
        'pagina/logout/',
        logout_html,
        name='logout-html'
    ),
    path(
        'pagina/registro/',
        registro,
        name='registro-html'
    ),
]