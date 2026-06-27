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


def get_featured_post():
    """Get featured published post."""
    return BlogPost.objects.filter(
        published_at__lte=timezone.now(), is_featured=True
    ).select_related("category", "author").first()


def get_recent_posts(exclude_slug=None, limit=5):
    """Get recent published posts, optionally excluding one."""
    qs = get_published_posts()
    if exclude_slug:
        qs = qs.exclude(slug=exclude_slug)
    return qs[:limit]


def get_all_categories():
    """Get all blog categories."""
    return BlogCategory.objects.all().order_by("name")