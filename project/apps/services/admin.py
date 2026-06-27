"""Admin for services with inline benefits and deliverables."""

from django.contrib import admin

from .models import Service, ServiceBenefit, ServiceDeliverable


class BenefitInline(admin.TabularInline):
    model = ServiceBenefit
    extra = 1


class DeliverableInline(admin.TabularInline):
    model = ServiceDeliverable
    extra = 1


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "order")
    list_filter = ("is_active",)
    search_fields = ("title", "short_description")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("technologies", "industries")
    inlines = [BenefitInline, DeliverableInline]
