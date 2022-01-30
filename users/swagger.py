"""
Copyright (c) 2022 Adam Lisichin, Hubert Decyusz, Wojciech Nowicki, Gustaw Daczkowski

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

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
