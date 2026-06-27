"""
Account models — user roles are managed via Django's built-in auth Groups.
No custom user model is needed; the project uses ``django.contrib.auth.models.User``
with Group-based permissions seeded by the ``seed`` management command.
"""
