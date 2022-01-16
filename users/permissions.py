"""
author: Adam Lisichin

description: Contains custom permissions.

permissions:
    - CurrentUserOrAdminPermission
"""
from django.views import View
from rest_framework.permissions import BasePermission
from rest_framework.request import Request

from users.models import User


class CurrentUserOrAdminPermission(BasePermission):
    """Custom permission which checks if request.user is an owner of the object or a superuser"""

    def has_object_permission(self, request: Request, view: View, obj: User):
        return request.user == obj or request.user.is_superuser
