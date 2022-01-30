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

description: File registers api endpoints

endpoints:
    - /api/auth/token/
    - /api/auth/token/refresh/
    - /api/auth/token/verify/
    - /api/auth/logout/
    - /api/users/
    - /api/users/<id>/
    - /api/users/me/
"""
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    JWTLogoutView,
    JWTObtainPairView,
    JWTRefreshView,
    JWTVerifyView,
    GetCurrentUser,
    UserViewSet,
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('auth/token/', JWTObtainPairView.as_view()),
    path('auth/token/refresh/', JWTRefreshView.as_view()),
    path('auth/token/verify/', JWTVerifyView.as_view()),
    path('auth/logout/', JWTLogoutView.as_view()),

    path('users/me/', GetCurrentUser.as_view({'get': 'retrieve'})),
    *router.urls,
]
