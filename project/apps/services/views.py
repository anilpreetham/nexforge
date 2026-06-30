"""Read-only DRF viewset for services."""

from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Service
from .serializers import ServiceDetailSerializer, ServiceListSerializer


class ServiceViewSet(ReadOnlyModelViewSet):
    """Public, read-only access to active services."""

    lookup_field = "slug"
    permission_classes = [AllowAny]
    search_fields = ["title", "short_description"]

    def get_queryset(self):
        qs = Service.objects.filter(is_active=True)
        if self.action == "retrieve":
            qs = qs.prefetch_related("technologies", "industries", "benefits", "deliverables")
        return qs

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ServiceDetailSerializer
        return ServiceListSerializer
