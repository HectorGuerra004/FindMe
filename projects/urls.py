from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserRegisterView,
    UserDetailView,
    ProfileViewSet,
    EducationViewSet,
    LikeViewSet,
    LoginView,
    LogoutView
)

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet)
router.register(r'educations', EducationViewSet)
router.register(r'likes', LikeViewSet)

urlpatterns = [
    path('register/', UserRegisterView.as_view()),
    path('user/', UserDetailView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('', include(router.urls)),
]