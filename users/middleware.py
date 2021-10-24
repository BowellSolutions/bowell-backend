class AuthorizationHeaderMiddleware:
    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        access_token = request.COOKIES.get('access')

        if access_token:
            request.META['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'

        return self.get_response(request)
