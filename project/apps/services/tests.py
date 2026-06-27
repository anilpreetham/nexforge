"""Tests for the services API."""

from rest_framework import status
from rest_framework.test import APITestCase

from .models import Service


class ServiceAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        Service.objects.create(title="PLC Programming", is_active=True)
        Service.objects.create(title="Hidden Service", is_active=False)

    def test_list_excludes_inactive(self):
        res = self.client.get("/api/v1/services/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["count"], 1)

    def test_detail_by_slug(self):
        res = self.client.get("/api/v1/services/plc-programming/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["title"], "PLC Programming")

    def test_slug_autofills(self):
        s = Service.objects.create(title="Machine Vision")
        self.assertEqual(s.slug, "machine-vision")
