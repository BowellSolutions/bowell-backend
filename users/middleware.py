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

description: Definition of AuthorizationHeaderMiddleware which injects access cookie from request into headers.
"""
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
