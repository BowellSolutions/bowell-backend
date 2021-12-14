from typing import Callable

from rest_framework.request import Request


class AuthorizationHeaderMiddleware:
    """Intercepts request and injects 'access' cookie into HTTP_AUTHORIZATION header"""

    def __init__(self, get_response: Callable = None):
        self.get_response = get_response

    def __call__(self, request: Request, *args, **kwargs):
        access_token = request.COOKIES.get('access')

        if access_token:
            request.META['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'

        return self.get_response(request)
