"""DRF serializers for services."""

from rest_framework import serializers

from .models import Service


class ServiceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ["id", "title", "slug", "short_description", "icon"]


class ServiceDetailSerializer(serializers.ModelSerializer):
    technologies = serializers.StringRelatedField(many=True)
    industries = serializers.StringRelatedField(many=True)
    benefits = serializers.StringRelatedField(many=True)
    deliverables = serializers.StringRelatedField(many=True)

    class Meta:
        model = Service
        fields = [
            "title",
            "slug",
            "short_description",
            "detailed_description",
            "icon",
            "technologies",
            "industries",
            "benefits",
            "deliverables",
        ]
