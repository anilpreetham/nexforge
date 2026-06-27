"""Selectors for services app - query layer."""

from apps.services.models import Service


def get_service_detail(slug):
    """Get service detail with all related data."""
    return Service.objects.prefetch_related(
        "technologies", "industries", "benefits", "deliverables"
    ).filter(slug=slug, is_active=True).first()


def get_active_services():
    """Get all active services ordered by order."""
    return Service.objects.filter(is_active=True).prefetch_related(
        "technologies", "industries"
    ).order_by("order")