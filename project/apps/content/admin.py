"""Admin for site content models."""

from django.contrib import admin

from .models import Award, Download, FAQ, GalleryItem, Testimonial


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "category", "order", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ("question", "answer")
    list_editable = ("order", "is_active")


@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "order")
    list_filter = ("category",)
    search_fields = ("title",)


@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    list_display = ("title", "year")
    list_filter = ("year",)
    search_fields = ("title",)


@admin.register(Download)
class DownloadAdmin(admin.ModelAdmin):
    list_display = ("title", "type", "created_at")
    list_filter = ("type",)
    search_fields = ("title",)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("author_name", "designation", "client", "is_active")
    list_filter = ("is_active",)
    search_fields = ("author_name", "quote")
