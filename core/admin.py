from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin

from .models import User
from . import forms


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = forms.UserChangeForm
    model = User
    list_display = [
        'id',
        'username',
        'email',
        'is_email_activated',
        'is_active',
        'is_staff',
    ]
    list_filter = [
        'username',
        'email',
    ]
    search_fields = [
        'username',
        'email',
    ]
    ordering = [
        'username',
        'email',
    ]
    fieldsets = [
        [
            None,
            {
                'fields': [
                    'email',
                    'username',
                    'password',
                ]
            },
        ],
        [
            'Permissions',
            {
                'fields': [
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                ],
            },
        ],
        [
            'Important dates',
            {
                'fields': [
                    'last_login',
                    'date_joined',
                ],
            },
        ],
    ]
    add_fieldsets = [
        [
            None,
            {
                'classes': [
                    'wide',
                ],
                'fields': [
                    'email',
                    'username',
                    'password1',
                    'password2',
                ],
            },
        ],
    ]
