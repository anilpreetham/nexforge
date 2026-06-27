"""DRF serializers for site content."""

from rest_framework import serializers

from .models import Award, Download, FAQ, GalleryItem, Testimonial


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ["id", "question", "answer", "category"]


class GalleryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryItem
        fields = ["id", "title", "category", "image"]


class AwardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Award
        fields = ["id", "title", "year", "description", "image"]


class DownloadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Download
        fields = ["id", "title", "file", "type", "created_at"]


class TestimonialSerializer(serializers.ModelSerializer):
    client = serializers.StringRelatedField()

    class Meta:
        model = Testimonial
        fields = ["id", "client", "author_name", "designation", "quote"]
