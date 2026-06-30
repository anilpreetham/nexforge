"""Admin registration for core lookup models."""

from django.contrib import admin

from .models import BranchOffice, Client, Industry, Technology


@admin.register(Industry)
class IndustryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ("name", "category")
    list_filter = ("category",)
    search_fields = ("name",)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("name", "industry", "website")
    list_filter = ("industry",)
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(BranchOffice)
class BranchOfficeAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "state", "country", "is_headquarters", "phone")
    list_filter = ("is_headquarters", "country")
    search_fields = ("name", "city")
