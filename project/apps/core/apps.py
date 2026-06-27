from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.core'

    def ready(self) -> None:
        """Import admin dashboard patch so analytics context is injected."""
        from . import admin_dashboard  # noqa: F401
