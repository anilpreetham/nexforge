"""Selectors for blog app - query layer."""

from django.utils import timezone

from apps.blog.models import BlogPost, BlogCategory


def get_published_posts():
    """Get all published blog posts with category and author."""
    return BlogPost.objects.filter(
        published_at__lte=timezone.now()
    ).select_related("category", "author").order_by("-published_at")


def get_post_detail(slug):
    """Get single published blog post by slug."""
    return BlogPost.objects.select_related("category", "author").filter(
        slug=slug, published_at__lte=timezone.now()
    ).first()


def get_all_categories():
    """Get all blog categories."""
    return BlogCategory.objects.all().order_by("name")