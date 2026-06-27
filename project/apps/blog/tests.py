"""Tests for the blog API."""

from datetime import timedelta

from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from .models import BlogCategory, BlogPost


class BlogAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.cat = BlogCategory.objects.create(name="Industry 4.0")
        BlogPost.objects.create(
            title="Published Post", category=cls.cat, body="x",
            published_at=timezone.now() - timedelta(days=1),
        )
        BlogPost.objects.create(
            title="Future Post", category=cls.cat, body="x",
            published_at=timezone.now() + timedelta(days=5),
        )
        BlogPost.objects.create(title="Draft Post", category=cls.cat, body="x")

    def test_list_only_shows_published(self):
        res = self.client.get("/api/v1/blog/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["count"], 1)
        self.assertEqual(res.data["results"][0]["title"], "Published Post")

    def test_detail_by_slug(self):
        res = self.client.get("/api/v1/blog/published-post/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("body", res.data)

    def test_draft_detail_404(self):
        res = self.client.get("/api/v1/blog/draft-post/")
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
