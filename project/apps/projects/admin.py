"""Admin for the projects portfolio with inline gallery/video/deliverables."""

from django.contrib import admin

from .models import (
    Project,
    ProjectDeliverable,
    ProjectGallery,
    ProjectMilestone,
    BeforeAfterGallery,
    ProjectVideo,
)


class GalleryInline(admin.TabularInline):
    model = ProjectGallery
    extra = 1


class VideoInline(admin.TabularInline):
    model = ProjectVideo
    extra = 1


class DeliverableInline(admin.TabularInline):
    model = ProjectDeliverable
    extra = 1


class MilestoneInline(admin.TabularInline):
    model = ProjectMilestone
    extra = 1


class BeforeAfterInline(admin.TabularInline):
    model = BeforeAfterGallery
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "industry", "status", "is_featured", "order")
    list_filter = ("status", "industry", "is_featured")
    search_fields = ("title", "overview", "location")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("technologies",)
    inlines = [GalleryInline, VideoInline, DeliverableInline, MilestoneInline, BeforeAfterInline]


@admin.register(ProjectMilestone)
class ProjectMilestoneAdmin(admin.ModelAdmin):
    list_display = ("title", "project", "date", "order")
    list_filter = ("project",)
    search_fields = ("title", "description")


@admin.register(BeforeAfterGallery)
class BeforeAfterGalleryAdmin(admin.ModelAdmin):
    list_display = ("project", "caption", "order")
    list_filter = ("project",)
