from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

from usuarios.models import Usuario

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serialzer personalizado para generar tokens JWT.
    
    Además de los claims estándar proporcionados por SimpleJWT, 
    se agrega el rol del usuario para que la API pueda identificar
    si el usuario autenticado es un cliente o un administrador.
    """
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Agregar el rol del usuario al token
        token['rol'] = user.rol
        return token
    
class RegistroUsuarioSerializer(serializers.ModelSerializer):
    """
    Serializer para el registro de nuevos usuarios.
    
    Por seguridad, todos los usuarios registrados a través de esta API serán asignados al rol de 'Cliente' por defecto.
    """
    password = serializers.CharField(
        write_only=True, 
        min_length=8, 
        help_text="La contraseña debe tener al menos 8 caracteres.", 
        style={'input_type': 'password'},
        )
    
    class Meta:
        model = Usuario
        fields = (
            'username', 
            'email', 
            'password', 
            'first_name', 
            'last_name',
        )
        
    def create(self, validated_data):
        """
        Crea un nuevo usuario utilizando create_user() para que
        Django aplique correctamente el hashing de la contraseña y establezca el rol como 'Cliente'.
        """
        usuario = Usuario.objects.create_user(
            **validated_data,
            rol=Usuario.Rol.CLIENTE,
        )
        
        return usuario