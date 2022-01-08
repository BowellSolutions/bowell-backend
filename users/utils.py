from urllib.parse import urlparse

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
    # values from settings
    is_production = not settings.DEBUG
    access_cookie_max_age = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds()
    refresh_cookie_max_age = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds()
    access_token_key = settings.SIMPLE_JWT['ACCESS_TOKEN_COOKIE']
    refresh_token_key = settings.SIMPLE_JWT['REFRESH_TOKEN_COOKIE']

    # get cookie domain
    if hasattr(settings, 'BACKEND_HOST'):
        host_url = settings.BACKEND_HOST
        domain = urlparse(host_url).netloc
        # removes subdomain e.g api.example.com -> .example.com
        cookie_domain = "." + ''.join(domain.split('.')[1:])
    else:
        cookie_domain = None

    # token can either be access or refresh
    max_age = access_cookie_max_age if is_access else refresh_cookie_max_age
    key = access_token_key if is_access else refresh_token_key

    return {
        "key": key,
        "value": token,
        "max_age": max_age,
        "expires": max_age,
        "secure": is_production,
        "httponly": True,
        "samesite": "None" if is_production else "Lax",
        "domain": cookie_domain,
        **kwargs
    }
