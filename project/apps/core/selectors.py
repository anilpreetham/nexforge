"""Selectors for core app - query layer."""

from apps.content.models import Award, Testimonial
from apps.core.models import Industry
from apps.projects.models import Project
from apps.services.models import Service


def get_featured_projects(limit=6):
    """Get featured projects with related industry."""
    return Project.objects.filter(is_featured=True).select_related("industry", "client")[:limit]


def get_active_services(limit=6):
    """Get active services."""
    return Service.objects.filter(is_active=True)[:limit]


def get_active_testimonials(limit=6):
    """Get active testimonials."""
    return Testimonial.objects.filter(is_active=True)[:limit]


def get_all_awards():
    """Get all awards ordered by year descending."""
    return Award.objects.all().order_by("-year")


def get_all_industries():
    """Get all industries ordered by name."""
    return Industry.objects.all().order_by("name")