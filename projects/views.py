from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User, Profile, Education, Like
from .serializers import (
    UserRegisterSerializer, UserSerializer,
    ProfileSerializer, EducationSerializer,
    LikeSerializer, LoginSerializer
)
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

class UserDetailView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class ProfileListCreateView(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

class EducationListCreateView(generics.ListCreateAPIView):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)

class LikeCreateView(generics.CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(from_profile=self.request.user.profile)

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                        context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
    
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data
        token, created = Token.objects.get_or_create(user=user)

        response = Response({
            'user': {
                'id': user.id,
                'email': user.email
                # Puedes añadir más campos del usuario si es necesario
            }
        }, status=status.HTTP_200_OK)

    # Configurar la cookie con el token
        response.set_cookie(
            key='auth_token',
            value=token.key,
            httponly=True,       # Importante para seguridad
            secure=True,         # Solo en producción con HTTPS
            samesite='Lax',      # Protección contra CSRF
            max_age=606024*7,  # Tiempo de expiración (ej. 1 semana)
        )

        return response


class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Eliminar el token del usuario
        Token.objects.filter(user=request.user).delete()

        # Crear respuesta
        response = Response(
            {'detail': 'Successfully logged out.'},
            status=status.HTTP_200_OK
        )

        # Eliminar la cookie del frontend
        response.delete_cookie(
            key='auth_token',
            path='/',
            samesite='Lax'
        )

        return response