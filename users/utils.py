"""
author: Adam Lisichin

description: Contains utility functions such as:
    - get_tokens_for_user
    - get_set_cookie_arguments
    - get_delete_cookie_arguments
"""
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user) -> tuple[str, str]:
    """
    Returns access and refresh token pair.
    access, refresh = get_tokens_for_user(user)
    """
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token), str(refresh)


def get_set_cookie_arguments(token: str, is_access: bool = True, **kwargs):
    """Returns dict with arguments passed to set_cookie function."""

    # values from settings
    access_cookie_max_age = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds()
    refresh_cookie_max_age = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds()
    access_token_key = settings.SIMPLE_JWT['ACCESS_TOKEN_COOKIE']
    refresh_token_key = settings.SIMPLE_JWT['REFRESH_TOKEN_COOKIE']

    # token can either be access or refresh
    max_age = access_cookie_max_age if is_access else refresh_cookie_max_age
    key = access_token_key if is_access else refresh_token_key

    return {
        "key": key,
        "value": token,
        "max_age": max_age,
        "expires": max_age,
        "secure": not settings.DEBUG,
        "httponly": True,
        "samesite": "None" if not settings.DEBUG else "Lax",
        "domain": settings.COOKIE_DOMAIN,
        **kwargs
    }


def get_delete_cookie_arguments(is_access: bool = True, **kwargs):
    """Returns dict with arguments passed to set_cookie function.
    Set_cookie with those arguments behaves like delete_cookie under the hood."""

    return {
        "key": "access" if is_access else "refresh",
        "value": "",
        "max_age": 0,
        "expires": 'Thu, 01 Jan 1970 00:00:00 GMT',
        "secure": not settings.DEBUG,
        "httponly": True,
        "samesite": "None" if not settings.DEBUG else "Lax",
        "domain": settings.COOKIE_DOMAIN,
        **kwargs
    }
