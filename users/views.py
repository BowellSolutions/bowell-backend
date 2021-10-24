from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK, HTTP_401_UNAUTHORIZED
)
from rest_framework.views import APIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView, TokenVerifyView
)

from users.serializers import CookieTokenRefreshSerializer, CookieTokenVerifySerializer


class JWTObtainPairView(TokenObtainPairView):
    """POST /api/auth/token/"""

    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get('access') and response.data.get('refresh'):
            access_cookie_max_age = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds()
            response.set_cookie(
                key=settings.SIMPLE_JWT['ACCESS_TOKEN_COOKIE'],
                value=response.data['access'],
                max_age=access_cookie_max_age,
                expires=access_cookie_max_age,
                secure=not settings.DEBUG,
                httponly=True
            )

            refresh_cookie_max_age = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds()
            response.set_cookie(
                key=settings.SIMPLE_JWT['REFRESH_TOKEN_COOKIE'],
                value=response.data['refresh'],
                max_age=refresh_cookie_max_age,
                expires=refresh_cookie_max_age,
                secure=not settings.DEBUG,
                httponly=True
            )
        return super().finalize_response(request, response, *args, **kwargs)


class JWTRefreshView(TokenRefreshView):
    """POST /api/auth/token/refresh/"""
    serializer_class = CookieTokenRefreshSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        if access_token := response.data.get('access'):
            access_cookie_max_age = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds()
            response.set_cookie(
                key=settings.SIMPLE_JWT['ACCESS_TOKEN_COOKIE'],
                value=access_token,
                max_age=access_cookie_max_age,
                expires=access_cookie_max_age,
                secure=not settings.DEBUG,
                httponly=True
            )
        return super().finalize_response(request, response, *args, **kwargs)


class JWTVerifyView(TokenVerifyView):
    """POST /api/auth/token/verify/"""
    serializer_class = CookieTokenVerifySerializer


class JWTLogoutView(APIView):
    """GET /api/auth/logout/"""

    def get(self, request, *args, **kwargs):
        if request.COOKIES.get('access') and request.COOKIES.get('refresh'):
            response = Response({'message': 'Logout successful!'}, status=HTTP_200_OK)
            # to do: blacklist those tokens
            response.delete_cookie('access')
            response.delete_cookie('refresh')
            return response
        return Response(
            {'message': 'Could not logout! Cookies \'access\'/\'refresh\' not found in request!'},
            status=HTTP_401_UNAUTHORIZED
        )


class TestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return Response({}, 200)

    def get(self, *args, **kwargs):
        return Response({}, 200)
