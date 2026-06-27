"""Email notifications for the contact flow."""

import logging

from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


def send_enquiry_email(enquiry) -> None:
    """Notify the sales inbox of a new enquiry.

    The DB record is the source of truth, so email failure must never lose a
    lead — ``fail_silently=True`` and we log instead of raising.
    """
    try:
        send_mail(
            subject=f"New enquiry from {enquiry.name}",
            message=f"{enquiry.message}\n\n{enquiry.email} | {enquiry.phone}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.SALES_INBOX],
            fail_silently=True,
        )
    except Exception:  # pragma: no cover - defensive; fail_silently covers most
        logger.exception("Failed to send enquiry email for enquiry %s", enquiry.pk)
