"""Project portfolio models."""

from django.db import models
from django.utils.text import slugify

from apps.core.models import TimeStamped


class Project(TimeStamped):
    """A delivered or ongoing automation project shown in the portfolio."""

    class Status(models.TextChoices):
        ONGOING = "ongoing", "Ongoing"
        COMPLETED = "completed", "Completed"

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    industry = models.ForeignKey(
        "core.Industry", on_delete=models.PROTECT, related_name="projects"
    )
    client = models.ForeignKey(
        "core.Client",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="projects",
    )
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.ONGOING
    )
    location = models.CharField(max_length=150, blank=True)
    project_value = models.CharField(max_length=80, blank=True)
    duration = models.CharField(max_length=60, blank=True)
    team_size = models.PositiveIntegerField(null=True, blank=True)
    overview = models.TextField(blank=True)
    challenges = models.TextField(blank=True)
    solution = models.TextField(blank=True)
    technologies = models.ManyToManyField(
        "core.Technology", blank=True, related_name="projects"
    )
    thumbnail = models.ImageField(upload_to="projects/thumbs/", blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order", "-created_at"]
        verbose_name = "project"
        verbose_name_plural = "projects"
        indexes = [models.Index(fields=["status", "is_featured"])]

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class ProjectGallery(models.Model):
    """An image attached to a project's gallery."""

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="gallery"
    )
    image = models.ImageField(upload_to="projects/gallery/")
    caption = models.CharField(max_length=180, blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name_plural = "project gallery"

    def __str__(self) -> str:
        return f"{self.project} image #{self.pk}"


class ProjectVideo(models.Model):
    """A video link attached to a project."""

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="videos"
    )
    video_url = models.URLField()
    title = models.CharField(max_length=150, blank=True)

    class Meta:
        ordering = ["pk"]
        verbose_name = "project video"
        verbose_name_plural = "project videos"

    def __str__(self) -> str:
        return self.title or self.video_url


class ProjectDeliverable(models.Model):
    """A concrete deliverable produced for a project."""

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="deliverables"
    )
    title = models.CharField(max_length=180)

    class Meta:
        ordering = ["pk"]
        verbose_name = "project deliverable"
        verbose_name_plural = "project deliverables"

    def __str__(self) -> str:
        return self.title


class ProjectMilestone(models.Model):
    """A key milestone or timeline entry for a project."""

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="milestones"
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date = models.DateField(null=True, blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order", "date"]

    def __str__(self) -> str:
        return f"{self.project.title} - {self.title}"


class BeforeAfterGallery(models.Model):
    """A before/after image pair for a project."""

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="before_after"
    )
    before_image = models.ImageField(upload_to="projects/before_after/")
    after_image = models.ImageField(upload_to="projects/before_after/")
    caption = models.CharField(max_length=180, blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name_plural = "before/after gallery"

    def __str__(self) -> str:
        return f"{self.project.title} - before/after #{self.pk}"
