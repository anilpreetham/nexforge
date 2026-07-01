"""Tests for the enquiry (contact/CRM) API."""

import string

from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Enquiry


class EnquiryAPITests(APITestCase):
    def setUp(self):
        # Enquiry endpoint is scope-throttled (5/min); the counter lives in the
        # cache and would otherwise bleed across test methods and 429.
        cache.clear()

    def test_public_can_create_enquiry(self):
        res = self.client.post(
            "/api/v1/enquiries/",
            {"name": "A", "email": "a@b.com", "message": "Hello there"},
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Enquiry.objects.count(), 1)
        self.assertEqual(Enquiry.objects.first().status, Enquiry.Status.NEW)
        # No type supplied -> defaults to GENERAL.
        self.assertEqual(Enquiry.objects.first().enquiry_type, Enquiry.Type.GENERAL)

    def test_enquiry_type_captured_and_validated(self):
        res = self.client.post(
            "/api/v1/enquiries/",
            {"name": "A", "email": "a@b.com", "message": "Book a slot",
             "enquiry_type": "factory_visit"},
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Enquiry.objects.first().enquiry_type, Enquiry.Type.FACTORY_VISIT)
        # Invalid choice rejected server-side.
        bad = self.client.post(
            "/api/v1/enquiries/",
            {"name": "A", "email": "a@b.com", "message": "Hello there",
             "enquiry_type": "hacker"},
        )
        self.assertEqual(bad.status_code, status.HTTP_400_BAD_REQUEST)

    def test_short_message_rejected(self):
        res = self.client.post(
            "/api/v1/enquiries/",
            {"name": "A", "email": "a@b.com", "message": "hi"},
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_anonymous_cannot_list_enquiries(self):
        res = self.client.get("/api/v1/enquiries/")
        self.assertIn(res.status_code, (status.HTTP_401_UNAUTHORIZED,
                                        status.HTTP_403_FORBIDDEN))

    def test_staff_can_list_enquiries(self):
        Enquiry.objects.create(name="A", email="a@b.com", message="Hello there")
        user = get_user_model().objects.create_user(
            "staff",
            password="".join(string.ascii_letters for _ in range(5)),
            is_staff=True,
        )
        self.client.force_authenticate(user=user)
        res = self.client.get("/api/v1/enquiries/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["count"], 1)
