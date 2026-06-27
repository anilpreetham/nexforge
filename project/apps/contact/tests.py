"""Tests for the enquiry (contact/CRM) API."""

import string

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Enquiry


class EnquiryAPITests(APITestCase):
    def test_public_can_create_enquiry(self):
        res = self.client.post(
            "/api/v1/enquiries/",
            {"name": "A", "email": "a@b.com", "message": "Hello there"},
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Enquiry.objects.count(), 1)
        self.assertEqual(Enquiry.objects.first().status, Enquiry.Status.NEW)

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
