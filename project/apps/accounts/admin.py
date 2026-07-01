"""Admin for Django auth groups.

The user model is now ``authentication.CustomUser``; its admin lives in the
authentication app. This module only customises the Group list.
"""

from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import Group

try:
    admin.site.unregister(Group)
except admin.sites.NotRegistered:
    pass


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin):
    list_display = ("name",)
    search_fields = ("name",)
