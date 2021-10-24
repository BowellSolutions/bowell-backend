from rest_framework_simplejwt.serializers import (
    TokenRefreshSerializer, TokenVerifySerializer
)


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
