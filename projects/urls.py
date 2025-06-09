from django.urls import path
from .views import (
    UserRegisterView, UserDetailView,
    ProfileListCreateView, ProfileDetailView,
    EducationListCreateView, LikeCreateView, LoginView, LogoutView
)

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),  # Nueva ruta
    path('me/', UserDetailView.as_view(), name='user-detail'),
    path('profiles/', ProfileListCreateView.as_view(), name='profile-list'),
    path('profiles/<int:pk>/', ProfileDetailView.as_view(), name='profile-detail'),
    path('educations/', EducationListCreateView.as_view(), name='education-list'),
    path('likes/', LikeCreateView.as_view(), name='like-create'),
    # +path('logout/', LogoutView.as_view(), name='logout'),
]