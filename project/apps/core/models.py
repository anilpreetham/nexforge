"""Shared lookup models used across the NexForge platform."""

from django.db import models


class TimeStamped(models.Model):
    """Abstract base adding created/updated timestamps."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Industry(models.Model):
    """A market/industry vertical that projects and services target."""

    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(unique=True)
    icon = models.ImageField(upload_to="industries/", blank=True, null=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "industries"

    def __str__(self) -> str:
        return self.name


class Technology(models.Model):
    """A technology/tool used to deliver projects and services."""

    name = models.CharField(max_length=120, unique=True)
    category = models.CharField(max_length=80, blank=True, db_index=True)
    icon = models.ImageField(upload_to="tech/", blank=True, null=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "technology"
        verbose_name_plural = "technologies"

    def __str__(self) -> str:
        return self.name


class Client(models.Model):
    """A NexForge customer that projects are delivered for."""

    name = models.CharField(max_length=180)
    slug = models.SlugField(unique=True)
    logo = models.ImageField(upload_to="clients/", blank=True, null=True)
    industry = models.ForeignKey(
        Industry,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="clients",
    )
    website = models.URLField(blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "client"

    def __str__(self) -> str:
        return self.name


class BranchOffice(models.Model):
    """A NexForge branch office location."""

    name = models.CharField(max_length=120)
    address = models.CharField(max_length=250, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, default="India")
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    is_headquarters = models.BooleanField(default=False, db_index=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "branch office"

    def __str__(self) -> str:
        return f"{self.name} ({self.city})"
