"""Read-only DRF viewsets for site content."""

from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Award, Download, FAQ, GalleryItem, Testimonial
from .serializers import (
    AwardSerializer,
    DownloadSerializer,
    FAQSerializer,
    GalleryItemSerializer,
    TestimonialSerializer,
)


class FAQViewSet(ReadOnlyModelViewSet):
    queryset = FAQ.objects.filter(is_active=True)
    serializer_class = FAQSerializer
    filterset_fields = ["category"]
    permission_classes = [AllowAny]


class GalleryItemViewSet(ReadOnlyModelViewSet):
    queryset = GalleryItem.objects.all()
    serializer_class = GalleryItemSerializer
    filterset_fields = ["category"]
    permission_classes = [AllowAny]


class AwardViewSet(ReadOnlyModelViewSet):
    queryset = Award.objects.all()
    serializer_class = AwardSerializer
    permission_classes = [AllowAny]


class DownloadViewSet(ReadOnlyModelViewSet):
    queryset = Download.objects.all()
    serializer_class = DownloadSerializer
    filterset_fields = ["type"]
    permission_classes = [AllowAny]


class TestimonialViewSet(ReadOnlyModelViewSet):
    queryset = Testimonial.objects.filter(is_active=True).select_related("client")
    serializer_class = TestimonialSerializer
    permission_classes = [AllowAny]
