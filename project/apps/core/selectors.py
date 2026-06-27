"""Selectors for core app - query layer."""

from apps.blog.models import BlogPost
from apps.content.models import Award, Download, FAQ, GalleryItem, Testimonial
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


def get_published_blog_posts(limit=None):
    """Get published blog posts with category and author."""
    from django.utils import timezone
    qs = BlogPost.objects.filter(published_at__lte=timezone.now()).select_related(
        "category", "author"
    )
    if limit:
        return qs[:limit]
    return qs


def get_blog_post_detail(slug):
    """Get single published blog post by slug."""
    from django.utils import timezone
    return BlogPost.objects.select_related("category", "author").filter(
        slug=slug, published_at__lte=timezone.now()
    ).first()


def get_active_faqs():
    """Get active FAQs ordered by order."""
    return FAQ.objects.filter(is_active=True).order_by("order")


def get_all_gallery_items():
    """Get all gallery items ordered by order."""
    return GalleryItem.objects.all().order_by("order")


def get_all_awards():
    """Get all awards ordered by year descending."""
    return Award.objects.all().order_by("-year")


def get_all_downloads():
    """Get all downloads ordered by created_at descending."""
    return Download.objects.all().order_by("-created_at")


def get_all_industries():
    """Get all industries ordered by name."""
    return Industry.objects.all().order_by("name")