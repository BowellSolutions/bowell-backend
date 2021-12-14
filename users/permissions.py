from django.views import View
from rest_framework.permissions import BasePermission
from rest_framework.request import Request

from users.models import User


class CurrentUserOrAdminPermission(BasePermission):
    def has_object_permission(self, request: Request, view: View, obj: User):
        return request.user == obj or request.user.is_superuser
