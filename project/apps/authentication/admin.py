from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import (
    CustomUser,
    Role,
    Permission,
    UserRole,
    RolePermission,
    RefreshToken,
)


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    """Proper user admin: hashes passwords and exposes staff/group controls.

    Registering CustomUser with a plain ModelAdmin would store passwords in
    plaintext and hide the permission fields, so we extend Django's UserAdmin.
    """

    list_display = ("username", "email", "first_name", "last_name", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active", "groups")
    search_fields = ("username", "email", "first_name", "last_name")

    # Add the extra CustomUser fields to the default UserAdmin layout.
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Profile", {"fields": ("phone_number", "profile_image")}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("Profile", {"fields": ("email", "phone_number")}),
    )


admin.site.register(Role)
admin.site.register(Permission)
admin.site.register(UserRole)
admin.site.register(RolePermission)
admin.site.register(RefreshToken)
