from rest_framework import viewsets, permissions, status
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
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated  # <-- Importación añadida

from rest_framework.decorators import action

from drf_spectacular.utils import extend_schema

# Permisos personalizados
class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS = GET, HEAD, OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user

class IsEducationOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.profile.user == request.user

# Vistas personalizadas (no ViewSet)
class UserRegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    
    @extend_schema(
        request=UserRegisterSerializer,
        responses=UserRegisterSerializer,
    )

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        responses=UserSerializer,
    )
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    @extend_schema(
        request=UserSerializer,
        responses=UserSerializer,
    )
    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ViewSets
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class EducationViewSet(viewsets.ModelViewSet):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    permission_classes = [permissions.IsAuthenticated, IsEducationOwner]

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['post']  # Solo permitir creación

    def perform_create(self, serializer):
        serializer.save(from_profile=self.request.user.profile)

# Vistas de autenticación
class LoginView(APIView):
    @extend_schema(
        request=LoginSerializer,
        responses=UserSerializer,
    )
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token, _ = Token.objects.get_or_create(user=user)

        response = Response({
            'user': UserSerializer(user).data
        }, status=status.HTTP_200_OK)

        response.set_cookie(
            key='auth_token',
            value=token.key,
            httponly=True,
            secure=True,
            samesite='Lax',
            max_age=604800  # 1 semana
        )
        return response

class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


    def post(self, request):
        request.user.auth_token.delete()
        response = Response({'detail': 'Successfully logged out.'})
        response.delete_cookie('auth_token')
        return response