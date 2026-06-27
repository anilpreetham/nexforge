"""Read-only DRF viewset for the blog."""

from django.utils import timezone
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import BlogPost
from .serializers import BlogDetailSerializer, BlogListSerializer


class BlogViewSet(ReadOnlyModelViewSet):
    """Public, read-only access to published blog posts."""

    lookup_field = "slug"
    permission_classes = [AllowAny]
    queryset = BlogPost.objects.none()  # set per-request in get_queryset
    filterset_fields = ["category__slug", "is_featured"]
    search_fields = ["title", "summary", "body"]

    def get_queryset(self):
        return (
            BlogPost.objects.filter(published_at__lte=timezone.now())
            .select_related("category", "author")
        )

    def get_serializer_class(self):
        if self.action == "retrieve":
            return BlogDetailSerializer
        return BlogListSerializer
