"""DRF serializers for the projects API."""

from rest_framework import serializers

from .models import Project, ProjectGallery, ProjectVideo


class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectGallery
        fields = ["image", "caption"]


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectVideo
        fields = ["video_url", "title"]


class ProjectListSerializer(serializers.ModelSerializer):
    """Compact representation for the portfolio grid."""

    industry = serializers.StringRelatedField()

    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "slug",
            "industry",
            "status",
            "location",
            "thumbnail",
            "is_featured",
        ]


class ProjectDetailSerializer(serializers.ModelSerializer):
    """Full representation for a single project page."""

    industry = serializers.StringRelatedField()
    client = serializers.StringRelatedField()
    technologies = serializers.StringRelatedField(many=True)
    deliverables = serializers.StringRelatedField(many=True)
    gallery = GallerySerializer(many=True, read_only=True)
    videos = VideoSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            "title",
            "slug",
            "industry",
            "client",
            "status",
            "location",
            "project_value",
            "duration",
            "overview",
            "challenges",
            "solution",
            "technologies",
            "deliverables",
            "gallery",
            "videos",
        ]
