from django.urls import path

from .views import (
    JWTLogoutView,
    JWTObtainPairView,
    JWTRefreshView,
    JWTVerifyView,
    TestView,
)

urlpatterns = [
    path('auth/token/', JWTObtainPairView.as_view()),
    path('auth/token/refresh/', JWTRefreshView.as_view()),
    path('auth/token/verify/', JWTVerifyView.as_view()),
    path('auth/logout/', JWTLogoutView.as_view()),

    # remove later
    path('auth/test/', TestView.as_view()),
]
