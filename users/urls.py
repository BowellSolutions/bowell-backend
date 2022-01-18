"""
author: Adam Lisichin

description: File registers api endpoints

endpoints:
    - /api/auth/token/
    - /api/auth/token/refresh/
    - /api/auth/token/verify/
    - /api/auth/logout/
    - /api/users/
    - /api/users/<id>/
    - /api/users/me/
"""
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    JWTLogoutView,
    JWTObtainPairView,
    JWTRefreshView,
    JWTVerifyView,
    GetCurrentUser,
    UserViewSet,
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('auth/token/', JWTObtainPairView.as_view()),
    path('auth/token/refresh/', JWTRefreshView.as_view()),
    path('auth/token/verify/', JWTVerifyView.as_view()),
    path('auth/logout/', JWTLogoutView.as_view()),

    path('users/me/', GetCurrentUser.as_view({'get': 'retrieve'})),
    *router.urls,
]
