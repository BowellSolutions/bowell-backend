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

description: Contains auth and user related serializers.

serializers:
    - CookieTokenRefreshSerializer
    - CookieTokenVerifySerializer
    - UserSerializer
    - RegisterUserSerializer
    - UpdateUserSerializer
"""
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import (
    TokenRefreshSerializer, TokenVerifySerializer
)

from users.validators import birth_date_validator

User = get_user_model()


class CookieTokenRefreshSerializer(TokenRefreshSerializer):
    """Serializer for refreshing JWT"""

    def validate(self, attrs):
        # If refresh token was found in cookies,
        # use it instead of the one from request body (request body can be empty)
        if refresh := self.context['request'].COOKIES.get('refresh'):
            attrs['refresh'] = refresh
        return super().validate(attrs)

    def create(self, validated_data):
        """Implementation required by abstract base class"""
        raise NotImplementedError()

    def update(self, instance, validated_data):
        """Implementation required by abstract base class"""
        raise NotImplementedError()


class CookieTokenVerifySerializer(TokenVerifySerializer):
    """Serializer for veryfing if JWT is valid"""

    def validate(self, attrs):
        # If refresh token was found in cookies,
        # use it instead of the one from request body (request body can be empty)
        if access := self.context['request'].COOKIES.get('access'):
            attrs['token'] = access
        return super().validate(attrs)

    def create(self, validated_data):
        """Implementation required by abstract base class"""
        raise NotImplementedError()

    def update(self, instance, validated_data):
        """Implementation required by abstract base class"""
        raise NotImplementedError()


class UserSerializer(serializers.ModelSerializer):
    """Serializer used for User representation"""

    class Meta:
        model = User
        exclude = ('password', 'groups', 'user_permissions')


class RegisterUserSerializer(serializers.ModelSerializer):
    """Serializer used for creating new user"""
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    birth_date = serializers.DateField(required=True, validators=[birth_date_validator])

    class Meta:
        model = User
        fields = (
            'email',
            'password',
            'first_name',
            'last_name',
            'birth_date',
            'type',
        )

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password'],
            birth_date=validated_data['birth_date'],
            type=validated_data['type'],
        )
        if user.type == user.Types.DOCTOR:
            # do not activate doctor account
            user.is_active = False
            user.save(update_fields=['is_active'])
        return user

    def to_representation(self, instance):
        # after submitting data, return data in format like in UserSerializer
        return UserSerializer(instance).data


class UpdateUserSerializer(serializers.ModelSerializer):
    """Serializer used for updating existing user's fields"""

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'birth_date',
        )

    def to_representation(self, instance):
        # after submitting data, return data in format like in UserSerializer
        return UserSerializer(instance).data
