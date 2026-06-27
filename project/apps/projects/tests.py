"""Tests for the projects API and models."""

from datetime import date

from django.db import models
from rest_framework import status
from rest_framework.test import APITestCase

from apps.core.models import Industry
from apps.projects.models import (
    BeforeAfterGallery,
    Project,
    ProjectMilestone,
)


class ProjectModelTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.auto = Industry.objects.create(name="Automotive", slug="automotive")
        cls.project = Project.objects.create(
            title="Test Project", industry=cls.auto, status="completed",
        )

    def test_project_str(self):
        self.assertEqual(str(self.project), "Test Project")

    def test_milestone_str(self):
        m = ProjectMilestone.objects.create(
            project=self.project,
            title="Design Complete",
            description="Finished the engineering design phase",
            date=date(2025, 6, 1),
            order=1,
        )
        self.assertIn("Test Project - Design Complete", str(m))

    def test_milestone_default_ordering(self):
        m2 = ProjectMilestone.objects.create(
            project=self.project, title="Z", order=2, date=date(2025, 7, 1),
        )
        m1 = ProjectMilestone.objects.create(
            project=self.project, title="A", order=1, date=date(2025, 6, 1),
        )
        qs = ProjectMilestone.objects.filter(project=self.project)
        self.assertEqual(list(qs), [m1, m2])

    def test_before_after_str(self):
        ba = BeforeAfterGallery.objects.create(
            project=self.project,
            before_image="projects/before_after/before.jpg",
            after_image="projects/before_after/after.jpg",
            caption="Line upgrade",
        )
        self.assertIn("Test Project - before/after", str(ba))

    def test_before_after_default_ordering(self):
        ba1 = BeforeAfterGallery.objects.create(
            project=self.project, order=1,
            before_image="projects/before_after/b1.jpg",
            after_image="projects/before_after/a1.jpg",
        )
        ba2 = BeforeAfterGallery.objects.create(
            project=self.project, order=0,
            before_image="projects/before_after/b2.jpg",
            after_image="projects/before_after/a2.jpg",
        )
        qs = BeforeAfterGallery.objects.filter(project=self.project)
        self.assertEqual(list(qs), [ba2, ba1])

    def test_milestone_m2m_relation_name(self):
        m = ProjectMilestone.objects.create(
            project=self.project, title="Kickoff",
        )
        self.assertIn(m, self.project.milestones.all())

    def test_before_after_relation_name(self):
        ba = BeforeAfterGallery.objects.create(
            project=self.project, order=0,
            before_image="projects/before_after/b.jpg",
            after_image="projects/before_after/a.jpg",
        )
        self.assertIn(ba, self.project.before_after.all())

    def test_milestone_fields(self):
        field_names = [f.name for f in ProjectMilestone._meta.get_fields()]
        for f in ("title", "description", "date", "order", "project"):
            self.assertIn(f, field_names)

    def test_before_after_fields(self):
        field_names = [f.name for f in BeforeAfterGallery._meta.get_fields()]
        for f in ("before_image", "after_image", "caption", "order", "project"):
            self.assertIn(f, field_names)


class ProjectAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.auto = Industry.objects.create(name="Automotive", slug="automotive")
        cls.pharma = Industry.objects.create(name="Pharma", slug="pharma")
        Project.objects.create(
            title="VoltEdge EV", industry=cls.auto, status="completed",
            is_featured=True, overview="EV line automation",
        )
        Project.objects.create(
            title="Medixa Pharma", industry=cls.pharma, status="ongoing",
        )

    def test_list_returns_all(self):
        res = self.client.get("/api/v1/projects/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["count"], 2)

    def test_filter_by_industry_slug(self):
        res = self.client.get("/api/v1/projects/?industry__slug=pharma")
        self.assertEqual(res.data["count"], 1)
        self.assertEqual(res.data["results"][0]["title"], "Medixa Pharma")

    def test_search_matches_overview(self):
        res = self.client.get("/api/v1/projects/?search=EV")
        self.assertEqual(res.data["count"], 1)

    def test_detail_by_slug(self):
        res = self.client.get("/api/v1/projects/voltedge-ev/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["title"], "VoltEdge EV")
        self.assertIn("gallery", res.data)

    def test_slug_autofills_from_title(self):
        p = Project.objects.create(title="New Line Robotics", industry=self.auto)
        self.assertEqual(p.slug, "new-line-robotics")
