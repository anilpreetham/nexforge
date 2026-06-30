"""Service catalogue models."""

from django.db import models
from django.utils.text import slugify


class Service(models.Model):
    """A service NexForge offers (e.g. PLC programming, IIoT integration)."""

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    short_description = models.TextField(blank=True)
    detailed_description = models.TextField(blank=True)
    icon = models.ImageField(upload_to="services/", blank=True, null=True)
    technologies = models.ManyToManyField(
        "core.Technology", blank=True, related_name="services"
    )
    industries = models.ManyToManyField(
        "core.Industry", blank=True, related_name="services"
    )
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "service"
        verbose_name_plural = "services"

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class ServiceBenefit(models.Model):
    """A selling-point benefit listed under a service."""

    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, related_name="benefits"
    )
    text = models.CharField(max_length=200)

    class Meta:
        ordering = ["pk"]
        verbose_name = "service benefit"
        verbose_name_plural = "service benefits"

    def __str__(self) -> str:
        return self.text


class ServiceDeliverable(models.Model):
    """A concrete deliverable a service produces."""

    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, related_name="deliverables"
    )
    title = models.CharField(max_length=180)

    class Meta:
        ordering = ["pk"]
        verbose_name = "service deliverable"
        verbose_name_plural = "service deliverables"

    def __str__(self) -> str:
        return self.title
