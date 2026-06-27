"""Reusable file-upload validators (server-side, enforced at the model layer)."""

from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.utils.deconstruct import deconstructible

# Allowed document types for downloads.
validate_document_extension = FileExtensionValidator(
    allowed_extensions=["pdf", "doc", "docx", "ppt", "pptx", "xls", "xlsx", "zip"]
)


@deconstructible
class MaxFileSizeValidator:
    """Reject uploads larger than ``max_mb`` megabytes."""

    def __init__(self, max_mb: int = 10) -> None:
        self.max_mb = max_mb

    def __call__(self, value) -> None:
        if value.size > self.max_mb * 1024 * 1024:
            raise ValidationError(
                f"File too large. Maximum size is {self.max_mb} MB."
            )

    def __eq__(self, other) -> bool:
        return isinstance(other, MaxFileSizeValidator) and self.max_mb == other.max_mb
