from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK, HTTP_401_UNAUTHORIZED
)
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView, TokenVerifyView
)

from users.serializers import CookieTokenRefreshSerializer, CookieTokenVerifySerializer


class JWTObtainPairView(TokenObtainPairView):
    """POST /api/auth/token/"""

    def finalize_response(self, request, response, *args, **kwargs):
        if access := response.data.get('access'):
            access_cookie_max_age = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds()
            response.set_cookie(
                key=settings.SIMPLE_JWT['ACCESS_TOKEN_COOKIE'],
                value=access,
                max_age=access_cookie_max_age,
                expires=access_cookie_max_age,
                secure=not settings.DEBUG,
                httponly=True
            )

        if refresh := response.data.get('refresh'):
            refresh_cookie_max_age = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds()
            response.set_cookie(
                key=settings.SIMPLE_JWT['REFRESH_TOKEN_COOKIE'],
                value=refresh,
                max_age=refresh_cookie_max_age,
                expires=refresh_cookie_max_age,
                secure=not settings.DEBUG,
                httponly=True
            )
        return super().finalize_response(request, response, *args, **kwargs)


class JWTRefreshView(TokenRefreshView):
    """POST /api/auth/token/refresh/"""
    serializer_class = CookieTokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        # if refresh cookie exists and refresh was not submitted via form/request
        if refresh := request.COOKIES.get('refresh') and not request.data.get('refresh'):
            _data = dict(request.data)
            _data.update({"refresh": str(refresh)})
            serializer = self.get_serializer(data=_data)
        else:
            serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=HTTP_200_OK)

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

    def post(self, request, *args, **kwargs):
        # if access cookie exists and token was not submitted via form/request
        if access := request.COOKIES.get('access') and not request.data.get('access'):
            _data = dict(request.data)
            _data.update({"token": str(access)})
            serializer = self.get_serializer(data=_data)
        else:
            serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=HTTP_200_OK)


class JWTLogoutView(APIView):
    """GET /api/auth/logout/"""

    def get(self, request, *args, **kwargs):
        if refresh := request.COOKIES.get('refresh'):
            response = Response({'message': 'Logout successful!'}, status=HTTP_200_OK)
            response.delete_cookie('access')

            refresh_token = RefreshToken(refresh)
            refresh_token.blacklist()
            response.delete_cookie('refresh')
            return response
        return Response(
            {'message': 'Could not logout! Cookie \'refresh\' not found in request!'},
            status=HTTP_401_UNAUTHORIZED
        )


class TestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return Response({}, 200)

    def get(self, *args, **kwargs):
        return Response({}, 200)
