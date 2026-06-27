"""Selectors for projects app - query layer."""

from apps.projects.models import Project


def get_project_detail(slug):
    """Get project detail with all related data."""
    return Project.objects.select_related("industry", "client").prefetch_related(
        "technologies", "gallery", "videos", "deliverables"
    ).filter(slug=slug).first()


def get_filtered_projects(filters=None):
    """Get projects filtered by status, industry, technology."""
    qs = Project.objects.select_related("industry", "client").prefetch_related(
        "technologies"
    )
    
    if filters:
        if filters.get("status"):
            qs = qs.filter(status=filters["status"])
        if filters.get("industry"):
            qs = qs.filter(industry__slug=filters["industry"])
        if filters.get("technology"):
            qs = qs.filter(technologies__name__icontains=filters["technology"])
        if filters.get("search"):
            from django.db.models import Q
            qs = qs.filter(
                Q(title__icontains=filters["search"]) |
                Q(overview__icontains=filters["search"]) |
                Q(location__icontains=filters["search"])
            )
    
    return qs.order_by("order", "-created_at")


def get_featured_projects(limit=3):
    """Get featured projects for homepage."""
    return Project.objects.filter(is_featured=True).select_related("industry")[:limit]


def get_related_projects(project, limit=3):
    """Get related projects from same industry."""
    return Project.objects.filter(
        industry=project.industry
    ).exclude(pk=project.pk).select_related("industry")[:limit]