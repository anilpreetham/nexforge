from apps.authentication.models import (
    UserRole,
    RolePermission,
)


class RoleService:
    DASHBOARD_MAP = {
        "Administrator": "admin.html",
        "HR Manager": "hr.html",
        "Sales Manager": "sales.html",
        "Content Manager": "cms.html",
        "Technical Support": "support.html",
    }

    @staticmethod
    def get_roles(user):
        """
        Returns a list of role names assigned to the user.
        """
        return list(
            UserRole.objects.filter(user=user)
            .values_list("role__name", flat=True)
        )

    @staticmethod
    def get_permissions(user):
        """
        Returns a unique list of permission codes assigned
        to the user through their roles.
        """
        return list(
            RolePermission.objects.filter(
                role__role_users__user=user
            )
            .values_list("permission__code", flat=True)
            .distinct()
        )

    @staticmethod
    def get_dashboard(user):
        """
        Returns the dashboard template based on the user's
        first assigned role.
        """
        roles = RoleService.get_roles(user)

        if not roles:
            return "/"

        return RoleService.DASHBOARD_MAP.get(
            roles[0],
            "/",
        )