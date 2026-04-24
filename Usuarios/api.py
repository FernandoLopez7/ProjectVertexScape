from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from Usuarios.models import User
from Usuarios.serializers import LoginSerializer
from rest_framework.authtoken.models import Token

class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')
        user = User.objects.filter(email=email).first()

        if user is None or not user.check_password(password):
            return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)

        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
