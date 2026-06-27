"""Tests for content app — selectors and API endpoints."""

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import SimpleTestCase
from rest_framework import status
from rest_framework.test import APITestCase

from apps.content.models import Award, Download, FAQ, GalleryItem, Testimonial
from apps.content.selectors import (
    get_active_faqs,
    get_active_testimonials,
    get_all_awards,
    get_faqs_by_category,
)


class FAQAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        FAQ.objects.create(question="Q1", answer="A1", category="general", is_active=True, order=1)
        FAQ.objects.create(question="Q2", answer="A2", category="service", is_active=True, order=2)
        FAQ.objects.create(question="Q3", answer="A3", category="general", is_active=False, order=3)

    def test_list_only_active(self):
        res = self.client.get("/api/v1/faqs/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["count"], 2)

    def test_filter_by_general_category(self):
        res = self.client.get("/api/v1/faqs/?category=general")
        self.assertEqual(res.data["count"], 1)
        self.assertEqual(res.data["results"][0]["question"], "Q1")

    def test_filter_by_service_category(self):
        res = self.client.get("/api/v1/faqs/?category=service")
        self.assertEqual(res.data["count"], 1)
        self.assertEqual(res.data["results"][0]["question"], "Q2")

    def test_get_active_faqs_selector(self):
        qs = get_active_faqs()
        self.assertEqual(qs.count(), 2)

    def test_get_faqs_by_category(self):
        qs = get_faqs_by_category("general")
        self.assertEqual(qs.count(), 1)


class GalleryAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        GalleryItem.objects.create(title="Factory Floor", category="projects", order=1)
        GalleryItem.objects.create(title="Control Room", category="projects", order=2)
        GalleryItem.objects.create(title="Team Photo", category="events", order=3)

    def test_list_all_items(self):
        res = self.client.get("/api/v1/gallery/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["count"], 3)

    def test_filter_by_category(self):
        res = self.client.get("/api/v1/gallery/?category=events")
        self.assertEqual(res.data["count"], 1)
        self.assertEqual(res.data["results"][0]["title"], "Team Photo")


class AwardAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        Award.objects.create(title="Best Automation", year=2024)
        Award.objects.create(title="Innovation Award", year=2025)

    def test_list_all_awards(self):
        res = self.client.get("/api/v1/awards/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["count"], 2)

    def test_get_all_awards_selector(self):
        qs = get_all_awards()
        self.assertEqual(qs.count(), 2)
        self.assertEqual(qs[0].year, 2025)


class DownloadAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        Download.objects.create(title="Company Profile", type="profile")
        Download.objects.create(title="PLC Brochure", type="brochure")
        Download.objects.create(title="Case Study A", type="case_study")

    def test_list_all_downloads(self):
        res = self.client.get("/api/v1/downloads/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["count"], 3)

    def test_filter_by_type(self):
        res = self.client.get("/api/v1/downloads/?type=brochure")
        self.assertEqual(res.data["count"], 1)
        self.assertEqual(res.data["results"][0]["title"], "PLC Brochure")


class TestimonialAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        Testimonial.objects.create(author_name="John", quote="Great work!", is_active=True)
        Testimonial.objects.create(author_name="Jane", quote="Excellent!", is_active=True)
        Testimonial.objects.create(author_name="Hidden", quote="Invisible", is_active=False)

    def test_list_only_active(self):
        res = self.client.get("/api/v1/testimonials/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["count"], 2)

    def test_returns_author_name(self):
        res = self.client.get("/api/v1/testimonials/")
        names = [r["author_name"] for r in res.data["results"]]
        self.assertIn("John", names)
        self.assertNotIn("Hidden", names)

    def test_get_active_testimonials_selector(self):
        qs = get_active_testimonials()
        self.assertEqual(qs.count(), 2)


class FileValidatorTests(SimpleTestCase):
    """Server-side upload validation for Download.file."""

    def test_extension_rejects_executable(self):
        from django.core.exceptions import ValidationError

        from apps.core.validators import validate_document_extension

        bad = SimpleUploadedFile("malware.exe", b"MZ")
        with self.assertRaises(ValidationError):
            validate_document_extension(bad)

    def test_extension_allows_pdf(self):
        from apps.core.validators import validate_document_extension

        ok = SimpleUploadedFile("profile.pdf", b"%PDF-1.4")
        validate_document_extension(ok)  # must not raise

    def test_size_limit_enforced(self):
        from django.core.exceptions import ValidationError

        from apps.core.validators import MaxFileSizeValidator

        big = SimpleUploadedFile("big.pdf", b"x" * (2 * 1024 * 1024))
        with self.assertRaises(ValidationError):
            MaxFileSizeValidator(1)(big)
