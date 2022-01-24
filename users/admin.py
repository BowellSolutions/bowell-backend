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

description: File registers custom User model and its model admin with custom forms (UserModify and UserCreate forms).
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UsernameField, UserCreationForm, UserChangeForm
from django.forms import EmailField
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.token_blacklist.admin import OutstandingTokenAdmin as BaseOutstandingTokenAdmin
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken

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


class OutstandingTokenAdmin(BaseOutstandingTokenAdmin):
    """Overrides simple_jwt's token admin, so that deleting users is possible."""

    def has_delete_permission(self, *args, **kwargs) -> bool:
        return True


admin.site.register(User, UserAdmin)

# unregister model and later register it with a new admin
admin.site.unregister(OutstandingToken)
admin.site.register(OutstandingToken, OutstandingTokenAdmin)
