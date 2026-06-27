"""Tests for core app — selectors and template views."""

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.core.models import Industry
from apps.core.selectors import (
    get_active_services,
    get_active_testimonials,
    get_all_industries,
    get_featured_projects,
)
from apps.projects.models import Project


class CoreSelectorTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.ind1 = Industry.objects.create(name="Automotive", slug="automotive")
        cls.ind2 = Industry.objects.create(name="Pharma", slug="pharma")

    def test_get_all_industries_ordered(self):
        qs = get_all_industries()
        self.assertEqual(qs.count(), 2)
        self.assertEqual(qs[0].name, "Automotive")

    def test_get_featured_projects_returns_empty(self):
        self.assertEqual(get_featured_projects(3).count(), 0)

    def test_get_featured_projects_with_data(self):
        p = Project.objects.create(
            title="Test Project",
            industry=self.ind1,
            is_featured=True,
            overview="Test overview",
        )
        qs = get_featured_projects(3)
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs[0], p)

    def test_get_featured_projects_excludes_non_featured(self):
        Project.objects.create(title="Non Featured", industry=self.ind1)
        self.assertEqual(get_featured_projects(3).count(), 0)

    def test_get_active_services_returns_empty(self):
        self.assertEqual(get_active_services(3).count(), 0)

    def test_get_active_testimonials_returns_empty(self):
        self.assertEqual(get_active_testimonials(3).count(), 0)


class CoreViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.ind = Industry.objects.create(name="Automotive", slug="automotive")

    def test_home_page_renders(self):
        res = self.client.get(reverse("home"))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertContains(res, "NexForge")
        self.assertContains(res, "Industries We Serve")

    def test_about_page_renders(self):
        res = self.client.get(reverse("about"))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertContains(res, "Innovation")

    def test_privacy_page_renders(self):
        res = self.client.get(reverse("privacy"))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_terms_page_renders(self):
        res = self.client.get(reverse("terms"))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_project_detail_404_for_unknown_slug(self):
        res = self.client.get(reverse("project-detail", kwargs={"slug": "nonexistent"}))
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_service_detail_404_for_unknown_slug(self):
        res = self.client.get(reverse("service-detail", kwargs={"slug": "nonexistent"}))
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_blog_detail_404_for_unknown_slug(self):
        res = self.client.get(reverse("blog-detail", kwargs={"slug": "nonexistent"}))
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_error_pages_use_custom_templates(self):
        res404 = self.client.get("/nonexistent-page-xyz/")
        self.assertEqual(res404.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("Page Not Found", res404.content.decode())
