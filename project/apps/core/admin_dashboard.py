"""Custom admin dashboard — patches the default AdminSite to add analytics."""

from datetime import timedelta

from django.contrib import admin
from django.utils import timezone

from apps.blog.models import BlogPost
from apps.contact.models import Enquiry
from apps.content.models import Award, Testimonial
from apps.projects.models import Project
from apps.services.models import Service


def _dashboard_data():
    """Return analytics context for the admin dashboard."""
    now = timezone.now()
    first_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    return {
        "project_count": Project.objects.count(),
        "completed_count": Project.objects.filter(status="completed").count(),
        "ongoing_count": Project.objects.filter(status="ongoing").count(),
        "enquiry_count": Enquiry.objects.count(),
        "recent_enquiry_count": Enquiry.objects.filter(
            created_at__gte=first_of_month
        ).count(),
        "blog_count": BlogPost.objects.count(),
        "service_count": Service.objects.filter(is_active=True).count(),
        "testimonial_count": Testimonial.objects.filter(is_active=True).count(),
        "award_count": Award.objects.count(),
        "recent_enquiries": Enquiry.objects.order_by("-created_at")[:5],
    }


# Monkey-patch each_context so dashboard data is available on every admin page
_orig_each_context = admin.site.each_context


def _patched_each_context(self, request):
    ctx = _orig_each_context(request)
    ctx.update(_dashboard_data())
    return ctx


admin.site.each_context = _patched_each_context.__get__(admin.site, type(admin.site))
