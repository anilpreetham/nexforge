"""Miscellaneous site content models: FAQ, gallery, awards, downloads, testimonials."""

from django.db import models

from apps.core.validators import MaxFileSizeValidator, validate_document_extension


class FAQ(models.Model):
    """A frequently-asked question."""

    class Category(models.TextChoices):
        GENERAL = "general", "General"
        SERVICE = "service", "Service"

    question = models.CharField(max_length=255)
    answer = models.TextField()
    category = models.CharField(
        max_length=20, choices=Category.choices, default=Category.GENERAL
    )
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self) -> str:
        return self.question


class GalleryItem(models.Model):
    """An image in the general site gallery."""

    title = models.CharField(max_length=180)
    category = models.CharField(max_length=80, blank=True)
    image = models.ImageField(upload_to="gallery/")
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "gallery item"
        verbose_name_plural = "gallery items"

    def __str__(self) -> str:
        return self.title


class Award(models.Model):
    """A company award or recognition."""

    title = models.CharField(max_length=200)
    year = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="awards/", blank=True, null=True)

    class Meta:
        ordering = ["-year"]
        verbose_name = "award"
        verbose_name_plural = "awards"

    def __str__(self) -> str:
        return f"{self.title} ({self.year})"


class Download(models.Model):
    """A downloadable document (profile, brochure, case study, report)."""

    class Type(models.TextChoices):
        PROFILE = "profile", "Company Profile"
        BROCHURE = "brochure", "Brochure"
        CASE_STUDY = "case_study", "Case Study"
        REPORT = "report", "Report"

    title = models.CharField(max_length=200)
    file = models.FileField(
        upload_to="downloads/",
        validators=[validate_document_extension, MaxFileSizeValidator(20)],
    )
    type = models.CharField(max_length=20, choices=Type.choices)
    project = models.ForeignKey(
        "projects.Project",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="downloads",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "download"
        verbose_name_plural = "downloads"

    def __str__(self) -> str:
        return self.title


class Testimonial(models.Model):
    """A client testimonial / quote."""

    client = models.ForeignKey(
        "core.Client",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="testimonials",
    )
    author_name = models.CharField(max_length=120)
    designation = models.CharField(max_length=120, blank=True)
    quote = models.TextField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-pk"]
        verbose_name = "testimonial"
        verbose_name_plural = "testimonials"

    __test__ = False

    def __str__(self) -> str:
        return self.author_name
