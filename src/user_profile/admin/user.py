from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from shared.django_admins.base_admin import BaseModelAdmin
from user_profile.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    search_fields = ["username", "email", "first_name", "last_name", "nickname"]
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            ("Personal info",),
            {"fields": ("first_name", "last_name", "email", "nickname")},
        ),
        (
            ("Permissions",),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (("Important dates",), {"fields": ("last_login", "date_joined")}),
    )
