"""
author: Adam Lisichin

description: File consists of serializers definition used only for swagger documentation.

Views provided by drf-simplejwt are not properly processed by drf-yasg,
so there is a need for custom response serializers.
"""
from rest_framework import serializers


class CookieTokenObtainPairResponseSerializer(serializers.Serializer):
    """Serializer used for swagger documentation.
    Return type of response at POST /api/auth/token/"""
    access = serializers.CharField()
    refresh = serializers.CharField()

    def create(self, validated_data):
        """Implementation required by abstract base class"""
        raise NotImplementedError()

    def update(self, instance, validated_data):
        """Implementation required by abstract base class"""
        raise NotImplementedError()


class CookieTokenRefreshResponseSerializer(serializers.Serializer):
    """Serializer used for swagger documentation.
    Return type of response at POST /api/auth/token/refresh/"""
    access = serializers.CharField()

    def create(self, validated_data):
        """Implementation required by abstract base class"""
        raise NotImplementedError()

    def update(self, instance, validated_data):
        """Implementation required by abstract base class"""
        raise NotImplementedError()


class CookieTokenVerifyResponseSerializer(serializers.Serializer):
    """Serializer used for swagger documentation.
    Return type of response at POST /api/auth/token/refresh/"""

    def create(self, validated_data):
        """Implementation required by abstract base class"""
        raise NotImplementedError()

    def update(self, instance, validated_data):
        """Implementation required by abstract base class"""
        raise NotImplementedError()
