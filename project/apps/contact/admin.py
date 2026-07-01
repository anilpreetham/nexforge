"""Admin for enquiries (CRM)."""

from django.contrib import admin

from .models import Enquiry


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "enquiry_type", "status", "assigned_to", "created_at")
    list_filter = ("enquiry_type", "status", "created_at")
    search_fields = ("name", "email", "message")
    list_editable = ("status",)
    readonly_fields = ("created_at",)
    date_hierarchy = "created_at"
