"""
author: Adam Lisichin

description: File registers custom User model and its model admin with custom forms (UserModify and UserCreate forms).
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UsernameField, UserCreationForm, UserChangeForm
from django.forms import EmailField
from django.utils.translation import gettext_lazy as _

from users.models import User


class CustomUsernameField(UsernameField):
    """UsernameField but without built-in value normalization if value is None"""

    def to_python(self, value):
        # do not perform any normalization if username is None or empty
        if not value:
            return
        # else normalize username
        return super().to_python(value)


class UserCreateForm(UserCreationForm):
    """Custom User Creation Form in Admin interface"""

    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "birth_date",
            "type",
        )
        field_classes = {'username': CustomUsernameField, 'email': EmailField}


class UserModifyForm(UserChangeForm):
    """Custom User Change Form in Admin interface"""

    class Meta:
        model = User
        fields = '__all__'
        field_classes = {'username': CustomUsernameField}


class UserAdmin(BaseUserAdmin):
    """Custom User Admin interface"""

    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'type')
    fieldsets = (
        (_('User details'), {'fields': ('email', 'username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'birth_date', 'type')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'first_name', 'last_name', 'birth_date', 'type', 'password1', 'password2'
            ),
        }),
    )
    form = UserModifyForm
    add_form = UserCreationForm


admin.site.register(User, UserAdmin)
