from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UsernameField, UserCreationForm
from django.forms import EmailField
from django.utils.translation import gettext_lazy as _

from users.models import User


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "birth_date",
            "type",
        )
        field_classes = {'username': UsernameField, 'email': EmailField}


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
    add_form = UserCreationForm


admin.site.register(User, UserAdmin)
