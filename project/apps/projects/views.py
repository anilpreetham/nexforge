"""Read-only DRF viewset for the projects portfolio."""

from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Project
from .serializers import ProjectDetailSerializer, ProjectListSerializer


class ProjectViewSet(ReadOnlyModelViewSet):
    """Public, read-only access to projects, filterable by industry/tech/status."""

    lookup_field = "slug"
    permission_classes = [AllowAny]
    pagination_class = None
    filterset_fields = ["status", "industry__slug", "technologies__name"]
    search_fields = ["title", "overview", "location"]

    def get_queryset(self):
        qs = Project.objects.select_related("industry", "client")
        if self.action == "retrieve":
            qs = qs.prefetch_related("technologies", "gallery", "videos", "deliverables")
        return qs

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ProjectDetailSerializer
        return ProjectListSerializer
