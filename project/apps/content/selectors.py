"""Selectors for content app - query layer."""

from apps.content.models import Award, Download, FAQ, Testimonial


def get_active_faqs():
    """Get active FAQs ordered by order."""
    return FAQ.objects.filter(is_active=True).order_by("order")


def get_faqs_by_category(category):
    """Get active FAQs filtered by category."""
    return FAQ.objects.filter(is_active=True, category=category).order_by("order")


def get_all_awards():
    """Get all awards ordered by year descending."""
    return Award.objects.all().order_by("-year")


def get_active_testimonials():
    """Get active testimonials with client."""
    return Testimonial.objects.filter(is_active=True).select_related("client")