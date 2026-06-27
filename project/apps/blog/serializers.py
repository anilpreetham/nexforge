"""DRF serializers for the blog."""

from rest_framework import serializers

from .models import BlogPost


class BlogListSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    author = serializers.StringRelatedField()

    class Meta:
        model = BlogPost
        fields = [
            "id",
            "title",
            "slug",
            "category",
            "author",
            "summary",
            "featured_image",
            "published_at",
        ]


class BlogDetailSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    author = serializers.StringRelatedField()

    class Meta:
        model = BlogPost
        fields = [
            "title",
            "slug",
            "category",
            "author",
            "summary",
            "body",
            "featured_image",
            "published_at",
        ]
