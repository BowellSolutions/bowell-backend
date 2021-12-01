from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import (
    TokenRefreshSerializer, TokenVerifySerializer
)

User = get_user_model()


class CookieTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        if refresh := self.context['request'].COOKIES.get('refresh'):
            attrs['refresh'] = refresh
        return super().validate(attrs)


class CookieTokenVerifySerializer(TokenVerifySerializer):
    def validate(self, attrs):
        if access := self.context['request'].COOKIES.get('access'):
            attrs['token'] = access
        return super().validate(attrs)


# to do
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)


# to do
class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'password',
            'email',
            'first_name',
            'last_name'
        )


# to do
class UpdateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=False, write_only=True, style={'input_type': 'password'})
    email = serializers.EmailField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = (
            'password',
            'email',
            'first_name',
            'last_name'
        )

    def to_representation(self, instance):
        # after submitting data, return data in format like in UserSerializer
        return UserSerializer(instance).data
