from django.urls import path
from .views import CustomTokenObtainPairView, RegistroUsuarioView
from rest_framework_simplejwt.views import TokenRefreshView

from .views import loging, logout, registro

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
        'login/',
        loging,
        name='loging'
    ),
    path(
        'logout/',
        logout,
        name='logout'
    ),
    path(
        'registro/',
        registro,
        name='registro'
    ),
]