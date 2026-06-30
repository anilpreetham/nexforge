"""Contact / CRM models."""

from django.conf import settings
from django.db import models


class Enquiry(models.Model):
    """A lead captured from the public contact form."""

    class Status(models.TextChoices):
        NEW = "new", "New"
        IN_PROGRESS = "in_progress", "In progress"
        CONVERTED = "converted", "Converted"
        CLOSED = "closed", "Closed"

    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    message = models.TextField()
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.NEW
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="enquiries",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["status"])]
        verbose_name = "enquiry"
        verbose_name_plural = "enquiries"

    def __str__(self) -> str:
        return f"{self.name} <{self.email}>"
